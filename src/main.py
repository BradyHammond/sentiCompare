# ================================================== #
#                        MAIN                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 11/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                     FILE SETUP                     #
# ================================================== #


# Import statements
from PyQt5 import QtWidgets
from src import UIMainWindow
import sys


# ================================================== #
#                        MAIN                        #
# ================================================== #

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UIMainWindow()
    ui.showWindow()
    sys.exit(app.exec_())

# ================================================== #
#                        EOF                         #
# ================================================== #