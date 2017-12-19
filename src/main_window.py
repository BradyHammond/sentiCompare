# ================================================== #
#                    MAIN WINDOW                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 11/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                     FILE SETUP                     #
# ================================================== #


# Import statements
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox
from src import FileDialog, SentimentAnalyzer


# ================================================== #
#                   CLASS DEFINITION                 #
# ================================================== #


# UIMainWindow class definition
class UIMainWindow(object):

    # Define __init__ function
    def __init__(self):
        # Create main window
        font = QtGui.QFont()
        font.setFamily("Myriad Pro")
        font.setPointSize(14)
        self.main_window = QtWidgets.QWidget()
        self.main_window.setFont(font)
        self.main_window.setObjectName("main_window")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.resize(450, 460)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.main_window.sizePolicy().hasHeightForWidth())
        self.main_window.setSizePolicy(size_policy)
        self.main_window.setMinimumSize(QtCore.QSize(450, 460))
        self.main_window.setMaximumSize(QtCore.QSize(450, 460))
        self.main_window.setBaseSize(QtCore.QSize(450, 460))

        # Create branding icon
        self.branding_icon = QtWidgets.QLabel(self.main_window)
        self.branding_icon.setGeometry(QtCore.QRect(20, 5, 90, 90))
        self.branding_icon.setText("")
        self.branding_icon.setPixmap(QtGui.QPixmap("../images/senticompare_logo.png"))
        self.branding_icon.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.branding_icon.setObjectName("branding_icon")

        # Create branding label
        self.branding_label = QtWidgets.QLabel(self.main_window)
        self.branding_label.setGeometry(QtCore.QRect(110, 5, 330, 90))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(81, 108, 146))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(81, 108, 146))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.branding_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Optima")
        font.setPointSize(50)
        self.branding_label.setFont(font)
        self.branding_label.setObjectName("branding_label")

        # Create first horizontal layout
        self.horizontal_layout_widget_1 = QtWidgets.QWidget(self.main_window)
        self.horizontal_layout_widget_1.setGeometry(QtCore.QRect(10, 410, 430, 50))
        self.horizontal_layout_widget_1.setObjectName("horizontal_layout_widget_1")
        self.horizontal_layout_1 = QtWidgets.QHBoxLayout(self.horizontal_layout_widget_1)
        self.horizontal_layout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_1.setObjectName("horizontal_layout_1")

        # Create run button
        self.run_button = QtWidgets.QPushButton(self.horizontal_layout_widget_1)
        self.run_button.setObjectName("run_button")
        self.run_button.clicked.connect(self.run)

        # Add run button to first horizontal layout
        self.horizontal_layout_1.addWidget(self.run_button)

        # Create quit button
        self.quit_button = QtWidgets.QPushButton(self.horizontal_layout_widget_1)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(self.main_window.close)

        # Add quit button to first horizontal layout
        self.horizontal_layout_1.addWidget(self.quit_button)

        # Create file selection tab
        self.select_files_tab = QtWidgets.QWidget()
        self.select_files_tab.setObjectName("select_files_tab")

        # Create second horizontal layout
        self.horizontal_layout_widget_2 = QtWidgets.QWidget(self.select_files_tab)
        self.horizontal_layout_widget_2.setGeometry(QtCore.QRect(10, 230, 230, 50))
        self.horizontal_layout_widget_2.setObjectName("horizontal_layout_widget_2")
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self.horizontal_layout_widget_2)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setObjectName("horizontal_layout_2")

        # Create input/output tab window
        font.setFamily("Myriad Pro")
        font.setPointSize(12)
        self.input_output_box = QtWidgets.QTabWidget(self.main_window)
        self.input_output_box.setGeometry(QtCore.QRect(10, 100, 260, 300))
        self.input_output_box.setFont(font)
        self.input_output_box.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.input_output_box.setTabPosition(QtWidgets.QTabWidget.North)
        self.input_output_box.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.input_output_box.setTabsClosable(False)
        self.input_output_box.setObjectName("input_output_box")

        # Create file view
        self.file_view = QtWidgets.QListView(self.select_files_tab)
        self.file_view.setGeometry(QtCore.QRect(10, 10, 235, 210))
        self.file_view.setObjectName("file_view")

        # Create file view model
        self.file_view_model = QStandardItemModel(self.file_view)

        # Add file view model to file view
        self.file_view.setModel(self.file_view_model)

        # Show file view
        self.file_view.show()

        # Add file selection tab to input/output tab window
        self.input_output_box.addTab(self.select_files_tab, "")

        # Create add button
        self.add_button = QtWidgets.QPushButton(self.horizontal_layout_widget_2)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.selectFiles)

        # Add add button to second horizontal layout
        self.horizontal_layout_2.addWidget(self.add_button)

        # Create delete button
        self.delete_button = QtWidgets.QPushButton(self.horizontal_layout_widget_2)
        self.delete_button.setFont(font)
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.removeFiles)

        # Add delete button to second horizontal layout
        self.horizontal_layout_2.addWidget(self.delete_button)

        # Create manual input tab
        self.manual_input_tab = QtWidgets.QWidget()
        self.manual_input_tab.setObjectName("manual_input_tab")

        # Create text input
        self.text_input = QtWidgets.QTextEdit(self.manual_input_tab)
        self.text_input.setGeometry(QtCore.QRect(10, 10, 235, 250))
        self.text_input.setObjectName("text_input")

        # Add text input to manual input tab
        self.input_output_box.addTab(self.manual_input_tab, "")

        # Create results tab
        self.results_tab = QtWidgets.QWidget()
        self.results_tab.setObjectName("results_tab")

        # Create results scroll box
        self.results_scroll_box = QtWidgets.QScrollArea(self.results_tab)
        self.results_scroll_box.setGeometry(QtCore.QRect(10, 10, 235, 250))
        self.results_scroll_box.setWidgetResizable(True)
        self.results_scroll_box.setObjectName("results_scroll_box")

        # Create results content
        self.results_content = QtWidgets.QWidget()
        self.results_content.setGeometry(QtCore.QRect(0, 0, 230, 250))
        self.results_content.setObjectName("results_content")
        self.results_scroll_box.setWidget(self.results_content)

        # Create results content text
        self.results_content_text = QtWidgets.QTextEdit(self.results_content)
        self.results_content_text.setGeometry(QtCore.QRect(-1, -1, 235, 250))
        self.results_content_text.setReadOnly(True)
        self.results_content_text.setObjectName("results_content_text")

        # Add results tab to input/output tab window
        self.input_output_box.addTab(self.results_tab, "")

        # Disable results tab
        self.input_output_box.setTabEnabled(2, False)

        # Create first group box
        font.setPointSize(14)
        self.group_box_1 = QtWidgets.QGroupBox(self.main_window)
        self.group_box_1.setGeometry(QtCore.QRect(280, 110, 160, 140))
        self.group_box_1.setFont(font)
        self.group_box_1.setTitle("")
        self.group_box_1.setAlignment(QtCore.Qt.AlignCenter)
        self.group_box_1.setFlat(False)
        self.group_box_1.setCheckable(False)
        self.group_box_1.setObjectName("group_box_1")

        # Create first vertical layout
        self.vertical_layout_widget_1 = QtWidgets.QWidget(self.group_box_1)
        self.vertical_layout_widget_1.setGeometry(QtCore.QRect(9, 0, 141, 141))
        self.vertical_layout_widget_1.setObjectName("vertical_layout_widget_1")
        self.vertical_layout_1 = QtWidgets.QVBoxLayout(self.vertical_layout_widget_1)
        self.vertical_layout_1.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_1.setObjectName("vertical_layout_1")

        # Create pronoun checkbox
        self.pronoun_checkbox = QtWidgets.QCheckBox(self.vertical_layout_widget_1)
        self.pronoun_checkbox.setFont(font)
        self.pronoun_checkbox.setObjectName("pronoun_checkbox")

        # Add pronoun checkbox to first vertical layout
        self.vertical_layout_1.addWidget(self.pronoun_checkbox)

        # Create lexical checkbox
        self.lexical_checkbox = QtWidgets.QCheckBox(self.vertical_layout_widget_1)
        self.lexical_checkbox.setFont(font)
        self.lexical_checkbox.setObjectName("lexical_checkbox")

        # Add lexical checkbox to first vertical layout
        self.vertical_layout_1.addWidget(self.lexical_checkbox)

        # Create rule based checkbox
        self.rule_based_checkbox = QtWidgets.QCheckBox(self.vertical_layout_widget_1)
        self.rule_based_checkbox.setFont(font)
        self.rule_based_checkbox.setObjectName("rule_based_checkbox")

        # Add rule_based checkbox to first vertical layout
        self.vertical_layout_1.addWidget(self.rule_based_checkbox)

        # Create machine learning checkbox
        self.machine_learning_checkbox = QtWidgets.QCheckBox(self.vertical_layout_widget_1)
        self.machine_learning_checkbox.setFont(font)
        self.machine_learning_checkbox.setObjectName("machine_learning_checkbox")

        # Add machine learning checkbox to first vertical layout
        self.vertical_layout_1.addWidget(self.machine_learning_checkbox)

        # Create help scroll box
        self.help_scroll_box = QtWidgets.QScrollArea(self.main_window)
        self.help_scroll_box.setGeometry(QtCore.QRect(280, 260, 160, 140))
        self.help_scroll_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.help_scroll_box.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.help_scroll_box.setWidgetResizable(True)
        self.help_scroll_box.setObjectName("help_scroll_box")

        # Create help content
        self.help_content = QtWidgets.QWidget()
        self.help_content.setGeometry(QtCore.QRect(0, 0, 158, 138))
        self.help_content.setObjectName("help_content")
        self.help_scroll_box.setWidget(self.help_content)

        # Create selected files variable
        self.selected_files = {}

        # Set current tab
        self.input_output_box.setCurrentIndex(0)

        # Retranslate UI
        self.retranslateUI()

        # Connect UI slots
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    # ============================================== #

    # Define retranslateUI function
    def retranslateUI(self):
        # Add text to ui elements
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("main_window", "SentiCompare"))
        self.add_button.setText(_translate("main_window", "Add"))
        self.delete_button.setText(_translate("main_window", "Delete"))
        self.input_output_box.setTabText(self.input_output_box.indexOf(self.select_files_tab),
                                         _translate("main_window", "Select Files"))
        self.input_output_box.setTabText(self.input_output_box.indexOf(self.manual_input_tab),
                                         _translate("main_window", "Manual Input"))
        self.input_output_box.setTabText(self.input_output_box.indexOf(self.results_tab),
                                         _translate("main_window", "Results"))
        self.run_button.setText(_translate("main_window", "Run"))
        self.quit_button.setText(_translate("main_window", "Quit"))
        self.pronoun_checkbox.setText(_translate("main_window", "Pronoun Usage"))
        self.lexical_checkbox.setText(_translate("main_window", "Lexical"))
        self.rule_based_checkbox.setText(_translate("main_window", "Rule Based"))
        self.machine_learning_checkbox.setText(_translate("main_window", "Machine Learning"))
        self.branding_label.setText(_translate("main_window", "SentiCompare"))

    # ============================================== #

    # Define showWindow function
    def showWindow(self):
        self.main_window.show()

    # ============================================== #

    # Define selectFiles function
    def selectFiles(self):
        # Create file dialog
        file_dialog = FileDialog(self.main_window)
        file_dialog.setFilters(["Text files (*.txt)"])
        file_dialog.setDefaultFilterIndex = 0
        file_dialog.setDefaultDirectory(os.path.expanduser('~'))
        file_dialog.exec()

        # Return if nothing was selected
        if file_dialog.getPath() == '':
            return

        # Add files from selected directory to file list
        elif file_dialog.getFilename()[2] == '':
            for file in os.listdir(file_dialog.getPath()):
                if file.endswith('.txt') and not file.startswith('.'):
                    file_path = os.path.join(file_dialog.getPath(), file)

                    if file_path not in self.selected_files:
                        self.selected_files[file] = file_path

                        item = QStandardItem(file)
                        item.setCheckable(True)
                        self.file_view_model.appendRow(item)

        # Add selected file to list
        else:
            if file_dialog.getPath() not in self.selected_files:
                self.selected_files[file_dialog.getFilename()[1]] = file_dialog.getPath()

                item = QStandardItem(file_dialog.getFilename()[1])
                item.setCheckable(True)
                self.file_view_model.appendRow(item)

    # ============================================== #

    # Define removeFiles function
    def removeFiles(self):
        # Remove all checked files
        for i in range(self.file_view_model.rowCount() - 1, -1, -1):
            if self.file_view_model.item(i).checkState():
                filename = self.file_view_model.item(i).text()
                del self.selected_files[filename]
                self.file_view_model.removeRow(i)

    # ============================================== #

    # Define run function
    def run(self):
        # Check if an analysis method is selected
        if not (self.pronoun_checkbox.isChecked() or self.lexical_checkbox.isChecked() or
                self.rule_based_checkbox.isChecked() or self.machine_learning_checkbox.isChecked()):
            # Create and show an error message
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Missing Parameters")
            message_box.setText("You haven't selected any methods of sentiment analysis. Please select at least one " +
                                "method from the list of options.")
            message_box.exec_()
            return

        # Check if the current tab is valid
        if self.input_output_box.currentIndex() == 2:
            # Create and show error message
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Select Input")
            message_box.setText("You must be on the \"Select Files\" page or the \"Manual Input\" page to run " +
                                "an analysis. Please select one of those pages and try again.")
            message_box.exec_()
            return

        else:
            progress_bar = QtWidgets.QProgressDialog("Running Sentiment Analysis...", "Cancel", 0, 100, self.main_window)
            progress_bar.setValue(0)
            progress_bar.setCancelButton(None)
            progress_bar.setWindowModality(QtCore.Qt.WindowModal)
            progress_bar.resize(400, 50)
            progress_bar.show()

            # Analyze selected files
            if self.input_output_box.currentIndex() == 0:
                sentiment_analyzer = SentimentAnalyzer(self.selected_files, progress_bar, pronoun=self.pronoun_checkbox.isChecked(),
                                                       lexical=self.lexical_checkbox.isChecked(),
                                                       rule_based=self.rule_based_checkbox.isChecked(),
                                                       machine_learning=self.machine_learning_checkbox.isChecked())

            # Analyze manual input
            else:
                sentiment_analyzer = SentimentAnalyzer(self.text_input.toPlainText(), progress_bar, pronoun=self.pronoun_checkbox.isChecked(),
                                                       lexical=self.lexical_checkbox.isChecked(),
                                                       rule_based=self.rule_based_checkbox.isChecked(),
                                                       machine_learning=self.machine_learning_checkbox.isChecked())

            results = sentiment_analyzer.runAnalyses()
            progress_bar.close()

            if results:
                self.results_content_text.setText(results)
                self.input_output_box.setTabEnabled(2, True)
                self.input_output_box.setCurrentIndex(2)

            else:
                message_box = QMessageBox()
                message_box.setIcon(QMessageBox.Warning)
                message_box.setWindowTitle("Missing Input")
                message_box.setText("You haven't added any input to analyze. Please select one or more files or " +
                                    "input some data manually.")
                message_box.exec_()
                return

# ================================================== #
#                        EOF                         #
# ================================================== #
