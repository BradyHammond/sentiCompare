# ================================================== #
#                 SENTIMENT ANALYZER                 #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 11/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                     FILE SETUP                     #
# ================================================== #


# Import statements
from multiprocessing import Value, Lock
import nltk
from nltk.corpus import sentiwordnet
from nltk.corpus.reader.wordnet import WordNetError
from nltk.stem import WordNetLemmatizer
import os
from PyQt5.QtWidgets import QMessageBox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

# SentimentAnalyzer class definition
class SentimentAnalyzer(object):
    # Define __init__ function
    def __init__(self, src, progress_bar, pronoun=False, lexical=False, rule_based=False, machine_learning=False):
        self.src = src
        self.progress_bar = progress_bar
        self.pronoun = pronoun
        self.lexical = lexical
        self.rule_based = rule_based
        self.machine_learning = machine_learning
        self.output = "===============================\n" + \
                      "                       ANALYSES SUMMARY\n" + \
                      "===============================\n"

        if self.machine_learning:
            tags = ['pos', 'neg']
            train_data = []
            train_labels = []
            for tag in tags:
                directory = "../data/" + tag
                for file in os.listdir("../data/" + tag):
                    with open(os.path.join(directory, file), 'r') as open_file:
                        content = open_file.read()
                        train_data.append(content)
                        train_labels.append(tag)

            self.vectorizer = TfidfVectorizer(min_df=5,
                                         max_df=0.8,
                                         sublinear_tf=True,
                                         use_idf=True)
            trained_vectors = self.vectorizer.fit_transform(train_data)
            self.classifier_rbf = svm.SVC()
            self.classifier_rbf.fit(trained_vectors, train_labels)

            self.classifier_linear = svm.SVC(kernel='linear')
            self.classifier_linear.fit(trained_vectors, train_labels)

            self.classifier_liblinear = svm.LinearSVC()
            self.classifier_liblinear.fit(trained_vectors, train_labels)


    # ============================================== #

    # Define runSentimentAnalyses function
    def runAnalyses(self):
        if self.src == '' or self.src == [] or self.src == {} or self.src is None:
            return False

        elif isinstance(self.src, str):
            tokenized_input = [nltk.word_tokenize(word) for word in self.src.split()]
            tagged_input = [nltk.pos_tag(token)[0] for token in tokenized_input]
            if self.pronoun:
                self.runPronounAnalysis(tagged_input)
            if self.lexical:
                self.runLexicalAnalysis(tagged_input)
            if self.rule_based:
                self.runRuleBasedAnalysis(self.src)
            if self.machine_learning:
                self.runMachineLearningAnalysis(self.src)
            self.progress_bar.setValue(100)

            return self.output
        else:
            progress = 0
            increment_value = 100/len(self.src)
            for k, v in self.src.items():
                try:
                    file = open(v, "r")
                    file_text = file.read()
                    file.close()
                except UnicodeDecodeError:
                    message_box = QMessageBox()
                    message_box.setIcon(QMessageBox.Critical)
                    message_box.setWindowTitle("Encoding Error")
                    message_box.setText("There was an error trying to read the file: \"" + v + "\". As a result " +
                                        " this file will be skipped.")
                    message_box.exec_()
                    continue

                self.output += "File: " + k + "\n"
                tokenized_input = [nltk.word_tokenize(word) for word in file_text.split()]
                tagged_input = [nltk.pos_tag(token)[0] for token in tokenized_input]

                if self.pronoun:
                    self.runPronounAnalysis(tagged_input)
                if self.lexical:
                    self.runLexicalAnalysis(tagged_input)
                if self.rule_based:
                    self.runRuleBasedAnalysis(file_text)
                if self.machine_learning:
                    self.runMachineLearningAnalysis(file_text)

                progress += increment_value
                self.progress_bar.setValue(progress)

            return self.output

    # ============================================== #

    # Define runPronounAnalysis Function
    def runPronounAnalysis(self, file):
        personal_pronouns = Counter(0)
        possessive_personal_pronouns = Counter(0)
        wh_pronouns = Counter(0)
        possessive_wh_pronouns = Counter(0)
        total_pronouns = Counter(0)
        word_count = Counter(0)

        self.calculatePronounCounts(personal_pronouns, possessive_personal_pronouns,
                                    wh_pronouns, possessive_wh_pronouns, total_pronouns,
                                    word_count, file)

        self.output += ("Personal Pronouns: " + str(personal_pronouns.value()) + "\n" +
                        "PP Frequency: " + "{0:.4f}".format(personal_pronouns.value() / word_count.value()) + "\n" +
                        "Possessive Personal Pronouns: " + str(possessive_personal_pronouns.value()) + "\n" +
                        "PPP Frequency: " + "{0:.4f}".format(
            possessive_personal_pronouns.value() / word_count.value()) + "\n" +
                        "Wh Pronouns: " + str(wh_pronouns.value()) + "\n" +
                        "WhP Frequency: " + "{0:.4f}".format(wh_pronouns.value() / word_count.value()) + "\n" +
                        "Possessive Wh Pronouns: " + str(possessive_wh_pronouns.value()) + "\n" +
                        "PWhP Frequency: " + "{0:.4f}".format(
            possessive_wh_pronouns.value() / word_count.value()) + "\n" +
                        "Total Pronouns: " + str(total_pronouns.value()) + "\n" +
                        "Total Pronoun Frequency: " + "{0:.4f}".format(
            total_pronouns.value() / word_count.value()) + "\n")

        if (0.005024*total_pronouns.value() + 0.2976) > 0.5:
            self.output += ("Sentiment Prediction: Positive\n" +
                            "-------------------------------------------------------------\n")
        else:
            self.output += ("Sentiment Prediction: Negative\n" +
                            "-------------------------------------------------------------\n")

    # ============================================== #

    # Define runLexicalAnalysis Function
    def runLexicalAnalysis(self, file):
        lemmatizer = WordNetLemmatizer()
        individual_scores = []
        multiple_scores = []
        # warning = False

        for tag in file:
            # if ("not" or "n't" in tag[0].lower()) and (not warning):
            #   self.output += "*** WARNING NEGATION DETECTED ***" + "\n" + \
            #                  "Lexical approach may not handle negation well. " + \
            #                  "As a result, this sentiment score may not be accurate" + "\n\n"
            #   warning = True

            lemma = lemmatizer.lemmatize(tag[0])
            if tag[1].startswith('NN'):
                syntag = 'n'
            elif tag[1].startswith('JJ'):
                syntag = 'a'
            elif tag[1].startswith('V'):
                syntag = 'v'
            elif tag[1].startswith('RB'):
                syntag = 'r'
            else:
                syntag = ''

            if syntag and syntag != '':
                try:
                    synset = sentiwordnet.senti_synset(lemma + "." + syntag + ".01")
                    score = synset.pos_score() - synset.neg_score()
                    individual_scores.append(score)
                except WordNetError:
                    pass

                score = 0
                synsets = list(sentiwordnet.senti_synsets(lemma, syntag))
                if len(synsets) > 0:
                    for syn in synsets:
                        score += syn.pos_score() - syn.neg_score()

                    multiple_scores.append(score / len(synsets))

        individual_score = self.standardizeScores(sum(individual_scores))
        multiple_score = self.standardizeScores(sum(multiple_scores))

        self.output += "Individual Synset Score: " + "{0:.4f}".format(individual_score) + "\n" + \
                       "Multiple Synset Score: " "{0:.4f}".format(multiple_score) + "\n" + \
                       "-------------------------------------------------------------\n"

    # ============================================== #

    # Define runRuleBasedAnalysis Function
    def runRuleBasedAnalysis(self, file):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(file)
        self.output += "Negative: " + str(scores['neg']) + "\n"
        self.output += "Neutral: " + str(scores['neu']) + "\n"
        self.output += "Positive: " + str(scores['pos']) + "\n"
        self.output += "Compount: " + str(scores['compound']) + "\n"
        self.output += "-------------------------------------------------------------\n"

    # ============================================== #

    # Define runMachineLearningAnalysis Function
    def runMachineLearningAnalysis(self, file):
        data_vector = self.vectorizer.transform([file])
        prediction_rbf = self.classifier_rbf.predict(data_vector)
        prediction_linear = self.classifier_linear.predict(data_vector)
        prediction_liblinear = self.classifier_liblinear.predict(data_vector)

        if prediction_rbf[0] == 'pos':
            self.output += "RBF Prediction: Positive\n"
        else:
            self.output += "RBF Prediction: Negative\n"

        if prediction_linear[0] == 'pos':
            self.output += "Linear Prediction: Positive\n"
        else:
            self.output += "Linear Prediction: Negative\n"

        if prediction_liblinear[0] == 'pos':
            self.output += "LibLinear Prediction: Positive\n"
        else:
            self.output += "LibLinear Prediction: Negative\n"
        self.output += "-------------------------------------------------------------\n"

    # ============================================== #

    # Define calculatePronounCounts Function
    def calculatePronounCounts(self, personal_pronouns, possessive_personal_pronouns,
                               wh_pronouns, possessive_wh_pronouns, total_pronouns,
                               word_count, file):
        for tag in file:
            if tag[1] != '.':
                word_count.increment()
                if tag[1] == 'PRP':
                    personal_pronouns.increment()
                    total_pronouns.increment()
                elif tag[1] == 'PRP$':
                    possessive_personal_pronouns.increment()
                    total_pronouns.increment()
                elif tag[1] == 'WP':
                    wh_pronouns.increment()
                    total_pronouns.increment()
                elif tag[1] == 'WP$':
                    possessive_wh_pronouns.increment()
                    total_pronouns.increment()

    # ============================================== #

    # Define standardizeScores Function
    def standardizeScores(self, score):
        if score > 1:
            score = 1.0000
        elif score < -1:
            score = -1.0000

        return score


class Counter(object):
    def __init__(self, init_value=0):
        self.val = Value('i', init_value)
        self.lock = Lock()

    # ============================================== #

    def increment(self):
        with self.lock:
            self.val.value += 1

    # ============================================== #

    def value(self):
        with self.lock:
            return self.val.value

# ================================================== #
#                        EOF                         #
# ================================================== #
