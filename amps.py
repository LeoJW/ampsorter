# AMPS
# Assited Motor Program Sorter (or Muscle Potential Sorter)
import json
import os
from PyQt6 import QtCore, QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QFileDialog,
    QHeaderView
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class TrialListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, trials=None, **kwargs):
        super(TrialListModel, self). __init__(*args, **kwargs)
        self.trials = trials or []
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            trial_num, trial_name = self.trials[index.row()]
            return trial_num
    def rowCount(self, index):
        return len(self.trials)

class MuscleTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(MuscleTableModel, self).__init__()
        self._data = data
        self.selected_trial_index = 0
    def setSelectedIndex(self, index):
        self.selected_trial_index = index
        self.layoutChanged.emit()
    def rowCount(self, index):
        # The length of the outer list
        return len(self._data[self.selected_trial_index])
    def columnCount(self, index):
        # Takes first sub-list of first trial, returns length
        # (only works if all rows are an equal length)
        return len(self._data[0][0])
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[self.selected_trial_index][index.row()][index.column()]


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.trialListModel = TrialListModel()
        # TODO: better initialization practice this seems dumb
        self.muscleTableModel = MuscleTableModel([[[]]]) 
        self.load()
        self.trialView.setModel(self.trialListModel)
        self.muscleView.setModel(self.muscleTableModel)
        # Connect the selection change in QListView to update the model
        self.trialView.selectionModel().currentChanged.connect(self.updateSelectedIndex)
        # self.trialView.clicked.connect(self.trial_clicked)
        self.muscleView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        #--- File menu 
        menu = self.menuBar()
        open_action = QAction("Open", self)
        open_action.setStatusTip("Open a new folder of data")
        open_action.triggered.connect(self.onFileOpenClick)
        
        load_action = QAction("Load", self)
        load_action.setStatusTip("Load previous spike sorting")
        load_action.triggered.connect(self.onFileOpenClick)
        
        file_menu = menu.addMenu("File")
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(load_action)
    
    def updateSelectedIndex(self, current, previous):
        self.muscleTableModel.setSelectedIndex(current.row())
    
    def onFileOpenClick(self, s):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Open Data Folder", "~")
        # TODO: db can save in location of app for now, but set name 
        # dynamic to moth file. 
        
        # TODO: logic to only do this if nothing open
        
        dir_contents = os.listdir(dir_path)
        # make dir for contents if none exists
        # if 'amps' not in dir_contents:
        # db_path = os.path.join(dir_path, 'amps')
        # os.mkdir(db_path)
        
        # Go to dir and grab list of trials
        trial_names = [f for f in dir_contents
                if 'FT' in f
                if '.mat' in f 
                if 'Control' not in f
                if 'quiet' not in f
                if 'empty' not in f]
        trial_nums = [f[-7:-4] for f in trial_names]
        trials = sorted(zip(trial_nums, trial_names))
        # Generate fresh (muscle, nspike) matrix
        muscles = ['lax','lba','lsa','ldvm','ldlm','rdlm','rdvm','rsa','rba','rax']
        muscle_table = [[[m, i] for m in muscles] for i in range(len(trials))]
        self.trialListModel.trials = trials
        self.muscleTableModel._data = muscle_table
        self.save()
        self.trialListModel.layoutChanged.emit()
        self.muscleTableModel.layoutChanged.emit()
        # self.load()
        # else:
            # Load contents that already exist
            
    
    def load(self):
        try:
            with open('data.db', 'r') as f:
                data = json.load(f)
                self.trialListModel.trials = data['trialListModel']
                self.muscleTableModel._data = data['muscleTableModel']
                self.trialListModel.layoutChanged.emit()
                self.muscleTableModel.layoutChanged.emit()
        except Exception:
            pass
    def save(self):
        with open('data.db', 'w') as f:
            data = {
                'trialListModel' : self.trialListModel.trials,
                'muscleTableModel' : self.muscleTableModel._data
                }
            json.dump(data, f)
    
    def trial_clicked(self, index):
        indexes = self.trialView.selectedIndexes()


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()