# AMPS
# Assited Motor Program Sorter (or Muscle Potential Sorter)
import json
import os
import scipy.io
import numpy as np
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QFileDialog,
    QHeaderView
)
import pyqtgraph as pg
from settingsDialog import *

#TODO: Load from previous actually set up full state (current selected muscles and trials)


qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

# Could set up to instead get names from files themselves
# Premature optimization is the root of all evil, though
muscleNames = ['lax','lba','lsa','ldvm','ldlm','rdlm','rdvm','rsa','rba','rax']
viewEnableColor = '#73A843'
highlightColor = '#EEEEEE'
muscleColors = {
    "lax" : "#94D63C", "rax" : "#6A992A",
    "lba" : "#AE3FC3", "rba" : "#7D2D8C",
    "lsa" : "#FFBE24", "rsa" : "#E7AC1E",
    "ldvm": "#66AFE6", "rdvm": "#2A4A78",
    "ldlm": "#E87D7A", "rdlm": "#C14434"
}

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
    def __init__(self, data=[[[]]]):
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
        # View mode is hidden last column, hidden by not being indexed here
        return len(self._data[0][0]) - 1
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[self.selected_trial_index][index.row()][index.column()]

# TODO: Model for spike times + units(?) + invalidated + waveforms

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.trialListModel = TrialListModel()
        self.muscleTableModel = MuscleTableModel() 
        self.trialView.setModel(self.trialListModel)
        self.muscleView.setModel(self.muscleTableModel)
        self._path_data = os.path.dirname(os.path.abspath(__file__))
        self._path_amps = os.path.dirname(os.path.abspath(__file__))
        # Traces plot
        self._activeIndex = 0
        self.traces = []
        self.traceData = {'time' : np.zeros((200000, 1))}
        for i,m in enumerate(muscleNames):
            pen = pg.mkPen(color=muscleColors[m])
            self.traceData[m] = np.zeros((200000))
            self.traces.append(self.traceView.plot([0],[0], pen=pen, name=m))
            self.traces[i].curve.metaData = m
            self.traces[i].setDownsampling(ds=1, auto=True, method='subsample')
            self.traces[i].setCurveClickable(True)
            self.traces[i].sigClicked.connect(self.traceClicked)
        self.traceView.showGrid(x=True, y=True)
        infline = pg.InfiniteLine(pos=1, angle=0, movable=True)
        self.traceView.addItem(infline)
        
        # Connect callback functions for changing selections
        self.trialView.selectionModel().currentChanged.connect(self.trialSelectionChanged)
        self.muscleView.selectionModel().selectionChanged.connect(self.updateTraceViewPlot)
        self.muscleView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        #--- Top toolbar menus
        menu = self.menuBar()
        open_action = QAction("Open", self)
        open_action.setStatusTip("Open a new folder of data")
        open_action.triggered.connect(self.onFileOpenClick)
        
        load_action = QAction("Load last session", self)
        load_action.setStatusTip("Load previous spike sorting session")
        load_action.triggered.connect(self.onLoadPreviousClick)
        
        settings_action = QAction("Preferences", self)
        settings_action.setStatusTip("Open window with advanced and extended settings")
        settings_action.triggered.connect(self.onSettingsClick)
        
        file_menu = menu.addMenu("File")
        settings_menu = menu.addMenu("Preferences")
        # Note: naming the settings_menu and settings_action the same name 
        # seems to trigger moving it to the more official Python > Preferences (Cmd + ,)
        # location. Not sure why, but it's nice so I'm leaving it
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(load_action)
        settings_menu.addAction(settings_action)
        settings_menu.addSeparator()
        
        #--- Settings dialog
        self.settingsDialog = SettingsDialog(self)
        
        #--- Keyboard shortcuts
        self.shortcutDict = {
            "Ctrl+O" : self.onFileOpenClick,
            "Ctrl+L" : self.onLoadPreviousClick,
            "Up" : self.nextTrace,
            "Down" : self.prevTrace
        }
        self.shortcuts = []
        for keycombo, keyfunc in self.shortcutDict.items():
            self.shortcuts.append(QShortcut(QKeySequence(keycombo), self))
            self.shortcuts[-1].activated.connect(keyfunc)
        
    def nextTrace(self):
        newindex = self._activeIndex + 1 if self._activeIndex < len(muscleNames) else self._activeIndex
        self.setActiveTrace(newindex)
    
    def prevTrace(self):
        newindex = self._activeIndex - 1 if self._activeIndex != 0 else self._activeIndex
        self.setActiveTrace(newindex)
    
    def setActiveTrace(self, index):
        prev = self._activeIndex
        # Change prev color back
        self.traces[prev].setPen(pg.mkPen(color=muscleColors[muscleNames[prev]]))
        # Set new selection to highlight color
        self.traces[index].setPen(pg.mkPen(color=highlightColor))
        self._activeIndex = index
    
    def traceClicked(self, evt):
        selectedMuscle = evt.curve.metaData
        self.setActiveTrace(muscleNames.index(selectedMuscle))
        
    def updateTraceViewPlot(self):
        selectedRowIndices = [item.row() for item in self.muscleView.selectionModel().selectedRows()]
        unselectedRowIndices = [i for i in set(range(len(muscleNames))) if i not in selectedRowIndices]
        # Plot selected traces
        for i,ind in enumerate(selectedRowIndices):
            self.traces[ind].setData(self.traceData['time'], self.traceData[muscleNames[ind]] + i)
        # Clear unselected traces
        for ind in unselectedRowIndices:
            self.traces[ind].setData([0],[0])
        # Update Y axis
        yax = self.traceView.getAxis('left')
        yax.setTicks([[(i, muscleNames[j]) for i,j in enumerate(selectedRowIndices)],[]])
        
    
    def trialSelectionChanged(self, current, previous):
        self.muscleTableModel.setSelectedIndex(current.row())
        # Retrieve selected trial's data 
        trial_name = self.trialListModel.trials[current.row()][1]
        fname = os.path.join(self._path_data, trial_name)
        file = scipy.io.loadmat(fname)
        # Grab data
        datamat = file[trial_name[0:-4]][:,0:11]
        # Get indices corresponding to each muscle name, save data
        channelNames = [column[0].lower() for column in file[trial_name[0:-4]+'_Header'][0][0][0][0]]
        inds = [channelNames.index(item) for item in muscleNames]
        for i,m in enumerate(muscleNames):
            # Normalize to amplitude of 1 before saving
            self.traceData[m] = datamat[:,inds[i]].reshape(-1) / (datamat[:,inds[i]].max() - datamat[:,inds[i]].min())
        self.traceData['time'] = datamat[:,0] # this might end up being too much of a special case
        # Update traceView plot
        self.updateTraceViewPlot()
    
    def onFileOpenClick(self):
        self._path_data = QFileDialog.getExistingDirectory(self, "Open Data Folder", "~")
        # TODO: logic to only do this if nothing open(?)
        self.initializeDataDir()
    
    def onLoadPreviousClick(self):
        # Get paths, core variables from QSettings
        settings = QtCore.QSettings('AgileSystemsLab', 'amps')
        self._path_data, self._path_amps = settings.value('last_paths', [], str)
        # Use those paths to populate app
        self.initializeDataDir()
        
    def onSettingsClick(self):
        self.settingsDialog.exec()
    
    def initializeDataDir(self):
        dir_contents = os.listdir(self._path_data)
        self._path_amps = os.path.join(self._path_data, 'amps')
        # If no dir for amps in data dir
        # Make one, read contents of data, populate app
        if 'amps' not in dir_contents:
            os.mkdir(self._path_amps)
            # Grab list of trials
            trial_names = [f for f in dir_contents
                    if '.mat' in f 
                    if 'FT' not in f
                    if 'Control' not in f
                    if 'quiet' not in f
                    if 'empty' not in f]
            trial_nums = [f[-7:-4] for f in trial_names]
            trials = sorted(zip(trial_nums, trial_names))
            # Generate fresh (muscle, nspike) matrix
            muscle_table = [[[m, i, False] for m in muscleNames] for i in range(len(trials))]
            self.trialListModel.trials = trials
            self.muscleTableModel._data = muscle_table
            self.save()
            self.trialListModel.layoutChanged.emit()
            self.muscleTableModel.layoutChanged.emit()
        # If there is amps dir, load that data
        else: 
            self.load()
    
    def load(self):
        try:
            with open(os.path.join(self._path_amps, 'params.db'), 'r') as f:
                data = json.load(f)
                self.trialListModel.trials = data['trialListModel']
                self.muscleTableModel._data = data['muscleTableModel']
                self.trialListModel.layoutChanged.emit()
                self.muscleTableModel.layoutChanged.emit()
        except Exception:
            pass
    def save(self):
        with open(os.path.join(self._path_amps, 'params.db'), 'w') as f:
            data = {
                'trialListModel' : self.trialListModel.trials,
                'muscleTableModel' : self.muscleTableModel._data
                }
            json.dump(data, f)
    
    def trial_clicked(self, index):
        indexes = self.trialView.selectedIndexes()
    
    # Execute on app close
    def closeEvent(self, event):
        settings = QtCore.QSettings('AgileSystemsLab', 'amps')
        settings.setValue('last_paths', [self._path_data, self._path_amps])


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()