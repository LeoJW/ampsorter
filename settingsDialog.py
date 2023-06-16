from PyQt6 import QtWidgets, QtCore, uic
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("settingsDialog.ui", self)
        
        self.settings = QtCore.QSettings('AgileSystemsLab', 'amps')
        
        self.waveformLengthLineEdit.setValidator(QIntValidator(1, 999, self))
        
        self.waveformLengthLineEdit.settingsKey = 'waveformLength'
        self.alignAtComboBox.settingsKey = 'alignAt'
        # Apply saved settings to all properties
        self.waveformLengthLineEdit.insert(self.settings.value('waveformLength', '32', str))
        self.alignAtComboBox.setCurrentText(self.settings.value('alignAt', 'local maxima', str))
        
        self.alignAtComboBox.currentTextChanged.connect(self.updateSettings)
        self.waveformLengthLineEdit.editingFinished.connect(self.updateSettings)
        
        self.activateWindow()
    
    def updateSettings(self):
        sender = self.sender()
        if isinstance(sender, QLineEdit):
            self.settings.setValue(sender.settingsKey, sender.text())
            sender.clearFocus()
        elif isinstance(sender, QComboBox):
            self.settings.setValue(sender.settingsKey, sender.currentText())
            sender.clearFocus()
    
    def closeEvent(self, event):
        self.settings.sync()
        print('Settings saved')