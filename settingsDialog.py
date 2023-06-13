from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QAction, QIcon, QIntValidator
from PyQt6.QtWidgets import (
    QPushButton
)

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("settingsDialog.ui", self)
        self.waveformLength.setValidator(QIntValidator(1, 999, self))
        # self.filedialog = QPushButton(self)
        # self.filedialog.setGeometry(QRect(10, 10, 50, 50))
        # self.filedialog.clicked.connect(self.dofunc)
        # self.resize(400, 700)
        self.activateWindow()
    def dofunc(self):
        print('damn')