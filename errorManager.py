from imports import *
import sklearn
import json
from PyQt5.QtWidgets import QMessageBox

def error(self, errorTitle, error):
        dialog = QMessageBox(self)
        dialog.setWindowTitle('An error has occurred')
        dialog.setText(errorTitle)
        dialog.setDetailedText(str(error))
        dialog.setMinimumHeight(500)
        dialog.setSizeIncrement(1, 1)
        dialog.setSizeGripEnabled(True)

        dialog.show()