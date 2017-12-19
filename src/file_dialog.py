# ================================================== #
#                    FILE DIALOG                     #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 11/26/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                     FILE SETUP                     #
# ================================================== #


# Import statements
import os
from PyQt5.QtWidgets import QFileDialog, QDialog


# ================================================== #
#                   CLASS DEFINITION                 #
# ================================================== #


# FileDialog class definition
class FileDialog(object):

    # Define __init__ function
    def __init__(self, main_window):
        self.main_window = main_window
        self.dialog = QFileDialog()
        self.directory = ''
        self.filename = ['', '', '']
        self.filters = []
        self.default_filter_index = 0
        self.path = ''

    # ============================================== #

    # Define path getter
    def getPath(self):
        return self.path

    # ============================================== #

    # Define filename getter
    def getFilename(self):
        return self.filename

    # ============================================== #

    # Define directory getter
    def getDirectory(self):
        return self.directory

    # ============================================== #

    # Define directory setter
    def setDefaultDirectory(self, value):
        self.directory = value

    # ============================================== #

    # Define filters getter
    def getFilters(self):
        return self.filters

    # ============================================== #

    # Define filters setter
    def setFilters(self, value):
        self.filters = value

    # ============================================== #

    # Define default filter index getter
    def getDefaultFilterIndex(self):
        return self.default_filter_index

    # ============================================== #

    # Define default filter index setter
    def setDefaultFilterIndex(self, value):
        self.default_filter_index = value

    # ============================================== #

    # Define exec function
    def exec(self, load=True):
        self.dialog.setNameFilters(self.filters)
        self.dialog.selectNameFilter(self.filters[self.default_filter_index])
        self.dialog.setDirectory(self.directory)
        if load:
            self.dialog.setLabelText(QFileDialog.Accept, 'Open')
            self.dialog.setWindowTitle('Open')
        else:
            self.dialog.setLabelText(QFileDialog.Accept, 'Save')
            self.dialog.setWindowTitle('Save')
        if self.dialog.exec() == QDialog.Accepted:
            self.path = self.dialog.selectedFiles()[0]
            filename = os.path.split(self.path)
            extension = os.path.splitext(self.path)[1]
            self.filename = [filename[0], filename[1], extension[1:len(extension)]]


# ================================================== #
#                        EOF                         #
# ================================================== #
