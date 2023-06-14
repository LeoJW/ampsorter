from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIntValidator

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("settingsDialog.ui", self)
        self.waveformLength.setValidator(QIntValidator(1, 999, self))
        self.activateWindow()
    def dofunc(self):
        print('damn')