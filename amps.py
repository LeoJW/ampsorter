# AMPS
# Assited Motor Program Sorter (or Muscle Potential Sorter)
import json
import dill
import datetime
import os
import scipy.io
from scipy.signal import butter, cheby1, cheby2, ellip, sosfreqz
import numpy as np
from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtGui import (
    QAction, 
    QKeySequence, 
    QShortcut, 
    QIntValidator, 
    QDoubleValidator,
    QFont,
    QColor
)
from PyQt6.QtWidgets import (
    QFileDialog,
    QHeaderView,
    QLineEdit,
    QLabel
)
import pyqtgraph as pg
from settingsDialog import *
from dataModels import *

#TODO: Load from previous actually set up full state (current selected muscles and trials)

# Main TODO:
# - json files save if program is opened and then closed. Catch this and prevent
# - Changing waveform length in the middle of sorting leads to save issue; np.concatenate can't combine arrays of different shape
# How can I set this up to toggle/stack different processing algorithms?

qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

# Could set up to instead get names from files themselves
# But premature optimization = root of all evil
muscleNames = ['lax','lba','lsa','ldvm','ldlm','rdlm','rdvm','rsa','rba','rax']
muscleNamesWithTime = ['time', *muscleNames]
filtEnableColor = '#73A843'
highlightColor = '#EEEEEE'
muscleColors = {
    "lax" : "#94D63C", "rax" : "#6A992A",
    "lba" : "#AE3FC3", "rba" : "#7D2D8C",
    "lsa" : "#FFBE24", "rsa" : "#E7AC1E",
    "ldvm": "#66AFE6", "rdvm": "#2A4A78",
    "ldlm": "#E87D7A", "rdlm": "#C14434"
}
unitColors = [
    '#ffffff', '#8dd3c7', 
    '#bebada', '#fb8072',
    '#80b1d3', '#fdb462',
    '#b3de69', '#fccde5',
    '#d9d9d9', '#bc80bd',
    '#ccebc5', '#ffed6f'
]
invalidColor = QColor(120,120,120,200)
unitKeys = ['0','1','2','3','4','5','6','7','8','9']
statusBarDisplayTime = 1000 # ms


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.trialListModel = TrialListModel()
        self.muscleTableModel = MuscleTableModel() 
        self.traceDataModel = TraceDataModel()
        self.spikeDataModel = SpikeDataModel()
        self.trialView.setModel(self.trialListModel)
        self.muscleView.setModel(self.muscleTableModel)
        self._path_data = os.path.dirname(os.path.abspath(__file__))
        self._path_amps = os.path.dirname(os.path.abspath(__file__))
        # Traces plot
        self._activeIndex = 0
        self.traces = []
        for i,m in enumerate(muscleNames):
            pen = pg.mkPen(color=muscleColors[m])
            self.traces.append(self.traceView.plot([],[], pen=pen, name=m))
            self.traces[i].curve.metaData = m
            self.traces[i].setDownsampling(ds=1, auto=True, method='subsample')
            self.traces[i].setCurveClickable(True)
            self.traces[i].sigClicked.connect(self.traceClicked)
        self.traceView.showGrid(x=True, y=True)
        self.thresholdLine = pg.InfiniteLine(pos=1, angle=0, movable=True)
        self.thresholdLine.setBounds((-0.5, 0.5))
        self.traceView.addItem(self.thresholdLine)
        self.thresholdLine.sigPositionChangeFinished.connect(self.thresholdChanged)
        # Waveform, spikes, PC plots 
        # For now assumes max of 10 units. Dumb but means units can be mapped to num keys
        self.waves = []
        self.spikes = []
        self.pcUnits = []
        for i in range(10):
            self.waves.append(self.waveView.plot([],[], pen=pg.mkPen(unitColors[i])))
            self.spikes.append(self.spikeView.plot([],[], pen=pg.mkPen(unitColors[i])))
            self.pcUnits.append(
                self.pcView.plot([],[], 
                    pen=None, symbolPen=None, 
                    symbol='o', symbolSize=3, symbolBrush=unitColors[i])
            )
            # self.spikes[i].sigPointsClicked(self.)
        # Extra last entry for invalid spikes/waves/pc points
        self.waves.append(self.waveView.plot([],[], pen=pg.mkPen(invalidColor)))
        self.spikes.append(self.spikeView.plot([],[], pen=pg.mkPen(invalidColor)))
        self.pcUnits.append(
            self.pcView.plot([],[], 
                pen=None, symbolPen=None, 
                symbol='o', symbolSize=3, symbolBrush=invalidColor)
        )
        # PC plot
        self.pcView.getPlotItem().getViewBox().setMouseMode(pg.ViewBox.RectMode)
        self.pcView.getPlotItem().getViewBox().sigSelectionReleased.connect(self.pcSelection)
        # Spikes plot
        self.spikeView.setXLink(self.traceView)
        self.spikeView.showAxes(False)
        self.spikeView.getPlotItem().getViewBox().setMouseMode(pg.ViewBox.RectMode)
        self.spikeView.getPlotItem().getViewBox().sigSelectionReleased.connect(self.spikeSelection)
        self.spikeView.setMouseEnabled(x=True, y=False)
        # Filter frequency response plot
        self.freqResponse = self.freqResponseView.plot([], [])
        self.freqResponseView.setLogMode(x=True, y=False)
        freqResponseTickFont = QFont('Times', 5)
        self.freqResponseView.getAxis('bottom').setStyle(tickFont=freqResponseTickFont)
        self.freqResponseView.getAxis('left').setStyle(tickFont=freqResponseTickFont)
        
        # Connect callback functions for trial/muscle view selection changes
        self.trialView.selectionModel().currentChanged.connect(self.trialSelectionChanged)
        self.muscleView.selectionModel().selectionChanged.connect(self.muscleSelectionChanged)
        self.muscleView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        #--- Filter controls
        self.updateFilter()
        self.passTypeComboBox.currentTextChanged.connect(self.updateFilter)
        self.filterTypeComboBox.currentTextChanged.connect(self.updateFilter)
        self.highpassCutoffHzLineEdit.editingFinished.connect(self.updateFilter)
        self.lowpassCutoffHzLineEdit.editingFinished.connect(self.updateFilter)
        self.orderLineEdit.editingFinished.connect(self.updateFilter)
        self.passbandRippleDBLineEdit.editingFinished.connect(self.updateFilter)
        self.stopbandAttenDBLineEdit.editingFinished.connect(self.updateFilter)
        self.highpassCutoffHzLineEdit.setValidator(QDoubleValidator(0.01, 5000.0, 3, self))
        self.lowpassCutoffHzLineEdit.setValidator(QDoubleValidator(0.01, 5000.0, 3, self))
        self.orderLineEdit.setValidator(QIntValidator(1, 20, self))
        self.passbandRippleDBLineEdit.setValidator(QDoubleValidator(0, 100, 3, self))
        self.stopbandAttenDBLineEdit.setValidator(QDoubleValidator(0, 100, 3, self))
        
        #--- Detection controls
        self.detectSpikesButton.clicked.connect(self.detectSpikes)
        self.undetectSpikesButton.clicked.connect(self.undetectSpikes)
        self.autosetThresholdsButton.clicked.connect(self.autosetThresholds)
        
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
        # Note: naming the settings_menu and settings_action the same name for macOS
        # triggers moving it to the more official Python > Preferences (Cmd + ,) location
        # Not sure why, but it's nice so I'm leaving it
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(load_action)
        settings_menu.addAction(settings_action)
        settings_menu.addSeparator()
        
        #--- Status bar
        self.fileLabel = QLabel('')
        self.statusBar.addPermanentWidget(self.fileLabel)
        
        #--- Settings dialog, main app settings
        self.settings = QtCore.QSettings('AgileSystemsLab', 'amps')
        self.settingsDialog = SettingsDialog(self)
        self.setSettingsCache()
        
        #--- Keyboard shortcuts
        self.shortcutDict = {
            "Ctrl+O" : self.onFileOpenClick,
            "Ctrl+L" : self.onLoadPreviousClick,
            "Ctrl+S" : self.save,
            "Ctrl+Up" : self.nextTrace,
            "Ctrl+Down" : self.prevTrace,
            "Ctrl+Shift+A" : self.autosetThresholds,
            "Up" : self.bumpThresholdUp,
            "Down" : self.bumpThresholdDown,
            "Alt+Up" : lambda: self.bumpThresholdUp(bump=0.05),
            "Alt+Down" : lambda: self.bumpThresholdDown(bump=0.05),
            "F" : self.filterTrace,
            "Ctrl+Shift+F" : self.autosetFilters,
            "Space" : self.detectSpikes,
            "Alt+Space" : self.undetectSpikes,
            "Ctrl+Shift+L" : self.autodetect,
            "Shift+Left" : self.panLeft,
            "Shift+Right" : self.panRight,
            "Shift+Up" : self.xZoomIn,
            "Shift+Down" : self.xZoomOut
        }
        self.shortcuts = []
        for keycombo, keyfunc in self.shortcutDict.items():
            self.shortcuts.append(QShortcut(QKeySequence(keycombo), self))
            self.shortcuts[-1].activated.connect(keyfunc)
    
    # Shift the trace view by default 5% of whatever the current range is
    def panLeft(self, frac=0.05):
        range = self.traceView.getPlotItem().viewRange()
        shift = frac * (range[0][1] - range[0][0])
        self.traceView.setXRange(range[0][0]-shift, range[0][1]-shift, padding=0)
    def panRight(self, frac=0.05):
        range = self.traceView.getPlotItem().viewRange()
        shift = frac * (range[0][1] - range[0][0])
        self.traceView.setXRange(range[0][0]+shift, range[0][1]+shift, padding=0)
    # Zoom in or out on the x axis by default 10% of current range
    def xZoomIn(self, frac=0.05):
        range = self.traceView.getPlotItem().viewRange()
        shift = frac * (range[0][1] - range[0][0])
        self.traceView.setXRange(range[0][0]+shift, range[0][1]-shift, padding=0)
    def xZoomOut(self, frac=0.05):
        range = self.traceView.getPlotItem().viewRange()
        shift = frac * (range[0][1] - range[0][0])
        self.traceView.setXRange(range[0][0]-shift, range[0][1]+shift, padding=0)
    
    def autodetect(self):
        self.autosetThresholds()
        if self.autoApplyFiltersRadioButton.isChecked():
            self.autosetFilters()
        noDetectMask = np.array([[arr.shape[0] <= 1 for arr in sublist] for sublist in self.spikeDataModel._spikes])
        for ti in range(noDetectMask.shape[0]):
            self.trialSelectionChanged(ti, None)
            for mi in range(noDetectMask.shape[1]):
                self.setActiveTrace(mi)
                self.detectSpikes()
    
    def autosetFilters(self):
        # Get which (trial, muscles) have been filtered and detection run
        detectMask = np.array([[arr.shape[0] > 1 for arr in sublist] for sublist in self.spikeDataModel._spikes])
        filterMask = np.array([[row[2] for row in sublist] for sublist in self.muscleTableModel._data])
        mask = np.logical_and(detectMask, filterMask)
        if np.any(mask):
            # Loop over muscles with filters applied
            muscleinds = np.where(np.any(mask, axis=0))[0]
            for mi in muscleinds:
                # Apply the farthest trial's filter to the remaining trials
                latestTrial = np.argmin(mask[:,mi], axis=0) - 1
                sos = self.spikeDataModel._filters[latestTrial][mi]
                for ti in np.arange(latestTrial, len(self.muscleTableModel._data)):
                    self.muscleTableModel._data[ti][mi][2] = True
                    self.spikeDataModel._filters[ti][mi] = sos
    
    def autosetThresholds(self):
        # Get which trial+muscles have been detected on
        # This might assume all trials have same # of muscles
        detectionRun = np.array([[arr.shape[0] > 1 for arr in sublist] for sublist in self.spikeDataModel._spikes])
        params = np.array(self.spikeDataModel._params)
        params[~detectionRun] = np.nan
        avgparam = np.nanmean(params, axis=0)
        avgparam[np.isnan(avgparam)] = 0.5 # set to default if none of this muscle ever set
        for i in range(params.shape[0]):
            for j in range(params.shape[1]):
                self.spikeDataModel._params[i][j] = avgparam[j]
        
    def spikeSelection(self, event):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if self.spikeDataModel._spikes[ti][mi].shape[0] <= 1:
            return
        lb, rb = event.rectCoords[0], event.rectCoords[2]
        mask = np.logical_and(
            self.spikeDataModel._spikes[ti][mi][:,0] >= lb,
            self.spikeDataModel._spikes[ti][mi][:,0] <= rb)
        if event.pressedKey in unitKeys:
            self.spikeDataModel._spikes[ti][mi][mask,1] = int(event.pressedKey)
        else:
            self.spikeDataModel._spikes[ti][mi][mask,2] = np.logical_not(self.spikeDataModel._spikes[ti][mi][mask,2])
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def pcSelection(self, event):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if self.spikeDataModel._spikes[ti][mi].shape[0] <= 1:
            return
        xl, yl, xu, yu = event.rectCoords
        # Get spikes within box
        xdata = self.spikeDataModel._pc[ti][mi][:,0]
        ydata = self.spikeDataModel._pc[ti][mi][:,1]
        mask = (xdata > xl) & (xdata < xu) & (ydata > yl) & (ydata < yu)
        if not np.any(mask):
            return
        if event.pressedKey in unitKeys:
            self.spikeDataModel._spikes[ti][mi][mask,1] = int(event.pressedKey)
        else:
            self.spikeDataModel._spikes[ti][mi][mask,2] = np.logical_not(self.spikeDataModel._spikes[ti][mi][mask,2])
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def updateSpikeView(self):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if self.spikeDataModel._spikes[ti][mi].shape[0] <= 1:
            for sp in self.spikes:
                sp.setData([], [], connect=np.array([1]))
            return
        unit = self.spikeDataModel._spikes[ti][mi][:,1]
        valid = self.spikeDataModel._spikes[ti][mi][:,2] == 1
        # Assume samples pre spike same across all spike waveforms
        samplesPreSpike = self.spikeDataModel._spikes[ti][mi][0,3]
        xvec = (np.arange(0, self.settingsCache['waveformLength']) - samplesPreSpike) / int(self.traceDataModel._fs)
        # Plot valid spikes for each unit
        for u in range(10):
            mask = np.logical_and(valid, unit==u)
            if not np.any(mask):
                self.spikes[u].setData([],[])
                continue
            nwaves = sum(mask)
            xdata = np.hstack([xvec + t for t in self.spikeDataModel._spikes[ti][mi][mask,0]])
            ydata = self.spikeDataModel._spikes[ti][mi][mask, 4:].ravel()
            singleConnected = np.ones(self.settingsCache['waveformLength'], dtype=np.int32)
            singleConnected[-1] = 0
            connected = np.tile(singleConnected, nwaves)
            self.spikes[u].setData(xdata, ydata, connect=connected)
        # Plot invalid waveforms, if they exist
        mask = np.logical_not(valid)
        if not np.any(mask):
            self.spikes[-1].setData([],[])
            return
        nwaves = sum(mask)
        ydata = self.spikeDataModel._spikes[ti][mi][mask, 4:].ravel()
        xdata = np.hstack([xvec + t for t in self.spikeDataModel._spikes[ti][mi][mask,0]])
        singleConnected = np.ones(self.settingsCache['waveformLength'], dtype=np.int32)
        singleConnected[-1] = 0
        connected = np.tile(singleConnected, nwaves)
        self.spikes[-1].setData(xdata, ydata, connect=connected)
    
    def updateWaveView(self):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if self.spikeDataModel._spikes[ti][mi].shape[0] <= 1:
            for w in self.waves:
                w.setData([], [], connect=np.array([1]))
            return
        unit = self.spikeDataModel._spikes[ti][mi][:,1]
        valid = self.spikeDataModel._spikes[ti][mi][:,2] == 1
        # Plot valid waveforms from each unit
        for u in range(10):
            mask = np.logical_and(valid, unit==u)
            if not np.any(mask):
                self.waves[u].setData([],[])
                continue
            nwaves = sum(mask)
            ydata = self.spikeDataModel._spikes[ti][mi][mask, 4:].ravel()
            xdata = np.tile(np.arange(self.settingsCache['waveformLength']), nwaves)
            singleConnected = np.ones(self.settingsCache['waveformLength'], dtype=np.int32)
            singleConnected[-1] = 0
            connected = np.tile(singleConnected, nwaves)
            self.waves[u].setData(xdata, ydata, connect=connected)
        # Plot invalid waveforms, if they exist
        mask = np.logical_not(valid)
        if not np.any(mask):
            return
        nwaves = sum(mask)
        ydata = self.spikeDataModel._spikes[ti][mi][mask, 4:].ravel()
        xdata = np.tile(np.arange(self.settingsCache['waveformLength']), nwaves)
        singleConnected = np.ones(self.settingsCache['waveformLength'], dtype=np.int32)
        singleConnected[-1] = 0
        connected = np.tile(singleConnected, nwaves)
        self.waves[-1].setData(xdata, ydata, connect=connected)
    
    def updatePCView(self):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if self.spikeDataModel._pc[ti][mi].shape[0] <= 1:
            for pcu in self.pcUnits:
                pcu.setData([],[])
            return
        unit = self.spikeDataModel._spikes[ti][mi][:,1]
        valid = self.spikeDataModel._spikes[ti][mi][:,2] == 1
        # Plot PC scores from each valid unit
        for u in range(10):
            mask = np.logical_and(valid, unit==u)
            if not np.any(mask):
                self.pcUnits[u].setData([],[])
                continue
            self.pcUnits[u].setData(self.spikeDataModel._pc[ti][mi][mask,0], self.spikeDataModel._pc[ti][mi][mask,1])
        # Plot invalid PC scores, if they exist
        mask = np.logical_not(valid)
        if not np.any(mask):
            return
        self.pcUnits[-1].setData(self.spikeDataModel._pc[ti][mi][mask,0], self.spikeDataModel._pc[ti][mi][mask,1])
    
    def updateTraceView(self):
        selectedRowIndices = [item.row() for item in self.muscleView.selectionModel().selectedRows()]
        unselectedRowIndices = [i for i in set(range(len(muscleNames))) if i not in selectedRowIndices]
        # Plot selected traces
        for i,ind in enumerate(selectedRowIndices):
            self.traces[ind].setData(self.traceDataModel.get('time'), self.traceDataModel.get(muscleNames[ind]) + i)
        # Clear unselected traces
        for ind in unselectedRowIndices:
            self.traces[ind].setData([],[])
        # Update Y axis
        yax = self.traceView.getAxis('left')
        yax.setTicks([[(i, muscleNames[j]) for i,j in enumerate(selectedRowIndices)],[]])
        # Set active index as one of the selected traces
        if self._activeIndex not in selectedRowIndices and len(selectedRowIndices) > 0:
            self.setActiveTrace(selectedRowIndices[0])
    
    def detectSpikes(self):
        self.statusBar.showMessage('detecting spikes', statusBarDisplayTime)
        muscleName = self.muscleTableModel._data[self.muscleTableModel.trialIndex][self._activeIndex][0]
        trialIndex, muscleIndex = self.muscleTableModel.trialIndex, self._activeIndex
        func = self.spikeDataModel._funcs[trialIndex][muscleIndex]
        params = self.spikeDataModel._params[trialIndex][muscleIndex]
        data = self.traceDataModel.get(muscleName)
        prespike = int(self.settingsCache['fractionPreAlign'] * self.settingsCache['waveformLength'])
        # If threshold is negative, flip both so we look for maximums
        # (Assumes params just single flat threshold)
        if params < 0:
            data = data.copy() # Otherwise actual data will get flipped
            data *= -1
            params *= -1
        # Find spikes by checking zero crossings of difference between threshold function and data
        crossvec = np.sign(func(self.traceDataModel.get('time'), params) - data)
        # Get where sign goes from +1 to -1
        inds = np.where(np.diff(crossvec) == -2.0)[0]
        # Remove last "spike" if too close to end
        if (inds[-1] + self.settingsCache['waveformLength']) > len(data):
            inds = np.delete(inds, -1)
        # Remove first "spikes" if too close to start
        removeinds = inds < prespike
        inds = inds[~removeinds,...]
        # Remove inds that don't meet dead time requirements
        difinds = np.diff(inds)
        keepinds = np.full(inds.shape, True)
        for i in range(len(difinds)-1):
            if difinds[i] <= self.settingsCache['deadTime']:
                keepinds[i+1] = False
                difinds[i+1] += difinds[i]
        # Last one has to be done separately as there's no next diff to add to
        keepinds[-1] = False if difinds[-1] <= self.settingsCache['deadTime'] else True
        inds = inds[keepinds,...]
        # Align each spike, save spike at each time
        # Spikes columns are [time, unit, valid, prespike, waveform...]
        spikes = np.zeros((len(inds), 4 + self.settingsCache['waveformLength']))
        if self.settingsCache['alignAt'] == 'local maxima':
            for i,ind in enumerate(inds):
                wave = data[ind:ind+self.settingsCache['waveformLength']]
                spikeind = np.argmax(wave) + ind
                wave = data[(spikeind-prespike):(spikeind+self.settingsCache['waveformLength']-prespike)]
                spikes[i,0] = self.traceDataModel.get('time')[spikeind]
                spikes[i,2] = 1
                spikes[i,3] = prespike
                spikes[i,4:] = wave
        elif self.settingsCache['alignAt'] == 'threshold crossing':
            for i,ind in enumerate(inds):
                wave = data[(ind-prespike):(ind+self.settingsCache['waveformLength']-prespike)]
                spikes[i,0] = self.traceDataModel.get('time')[ind]
                spikes[i,2] = 1
                spikes[i,3] = prespike
                spikes[i,4:] = wave
        self.spikeDataModel._spikes[trialIndex][muscleIndex] = spikes
        self.muscleTableModel._data[trialIndex][muscleIndex][1] = len(inds)
        self.muscleTableModel.layoutChanged.emit()
        self.spikeDataModel.updatePCA((trialIndex, muscleIndex))
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def undetectSpikes(self):
        ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        spikes = np.zeros((0, 4 + self.settingsCache['waveformLength']))
        self.spikeDataModel._spikes[ti][mi] = spikes
        self.muscleTableModel._data[ti][mi][1] = 0
        self.muscleTableModel.layoutChanged.emit()
        self.spikeDataModel.updatePCA((ti, mi))
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def updateFilter(self):
        order = int(self.orderLineEdit.text())
        passtype = self.passTypeComboBox.currentText()
        match passtype:
            case 'highpass':
                Wn = [float(self.highpassCutoffHzLineEdit.text())]
            case 'lowpass':
                Wn = [float(self.lowpassCutoffHzLineEdit.text())]
            case 'bandpass':
                Wn = [float(self.highpassCutoffHzLineEdit.text()), float(self.lowpassCutoffHzLineEdit.text())]
        # Special case where no real time vector: Rescale Wn assuming an actual rate of 10kHz
        if int(self.traceDataModel._fs) == 1.0:
            Wn = [i/5001 for i in Wn]
        match self.filterTypeComboBox.currentText():
            case 'butterworth':
                self._filtsos = butter(order, Wn, btype=passtype, fs=self.traceDataModel._fs, output='sos')
            case 'chebyshev1':
                rp = float(self.passbandRippleDBLineEdit.text())
                self._filtsos = cheby1(order, rp, Wn, btype=passtype, fs=self.traceDataModel._fs, output='sos')
            case 'chebyshev2':
                rs = float(self.stopbandAttenDBLineEdit.text())
                self._filtsos = cheby2(order, rs, Wn, btype=passtype, fs=self.traceDataModel._fs, output='sos')
            case 'elliptic':
                rp = float(self.passbandRippleDBLineEdit.text())
                rs = float(self.stopbandAttenDBLineEdit.text())
                self._filtsos = ellip(order, rp, rs, Wn, btype=passtype, fs=self.traceDataModel._fs, output='sos')
        # Plot frequency response
        w, h = sosfreqz(self._filtsos, worN=1500)
        db = 20*np.log10(np.maximum(np.abs(h), 1e-5))
        self.freqResponse.setData(w * self.traceDataModel._fs / (2 * np.pi), db)
        # Clear focus from LineEdit widgets if they triggered filter update
        if isinstance(self.sender(), QLineEdit):
            self.sender().clearFocus()
    
    def filterTrace(self, ti=None, mi=None, sos=None, changeFlag=True, plotUpdate=True):
        # Filter active trace with current filter by default
        if ti == None or mi == None:
            ti, mi = self.muscleTableModel.trialIndex, self._activeIndex
        if type(sos) is not np.ndarray:
            sos = self._filtsos
        activeMuscle = self.muscleTableModel._data[ti][mi][0]
        filtered = self.muscleTableModel._data[ti][mi][2]
        # Functon will either 
        # 1) Change trace's flag to filtered or unfiltered and either restore or filter trace
        # 2) Apply a filter to a trace without changing flag
        if changeFlag and filtered:
            self.traceDataModel.restore(activeMuscle)
            self.traceDataModel.normalize(activeMuscle)
        elif changeFlag and not filtered:
            self.spikeDataModel._filters[ti][mi] = sos
            self.traceDataModel.filter(activeMuscle, sos)
            self.traceDataModel.normalize(activeMuscle)
        elif not changeFlag:
            self.spikeDataModel._filters[ti][mi] = sos
            self.traceDataModel.filter(activeMuscle, sos)
            self.traceDataModel.normalize(activeMuscle)
        if changeFlag:
            self.muscleTableModel._data[ti][mi][2] = not filtered
            self.muscleTableModel.layoutChanged.emit()
        if plotUpdate:
            self.updateTraceView()
    
    # TODO: Could set to only move through currently displayed traces?
    def nextTrace(self):
        newindex = self._activeIndex + 1 if self._activeIndex < len(muscleNames) else self._activeIndex
        self.setActiveTrace(newindex)
    
    def prevTrace(self):
        newindex = self._activeIndex - 1 if self._activeIndex != 0 else self._activeIndex
        self.setActiveTrace(newindex)
    
    def traceClicked(self, event):
        selectedMuscle = event.curve.metaData
        self.setActiveTrace(muscleNames.index(selectedMuscle))
    
    def setActiveTrace(self, index):
        prev = self._activeIndex
        # Change prev color back
        self.traces[prev].setPen(pg.mkPen(color=muscleColors[muscleNames[prev]]))
        # Set new selection to highlight color
        self.traces[index].setPen(pg.mkPen(color=highlightColor))
        # Move threshold line/function to selected
        # Update this when more than just horizontal lines are allowed
        selectedRowIndices = [item.row() for item in self.muscleView.selectionModel().selectedRows()]
        if index in selectedRowIndices:
            newcenter = selectedRowIndices.index(index)
            newvalue = self.spikeDataModel._params[self.muscleTableModel.trialIndex][index]
            self.thresholdLine.setBounds((newcenter-0.5, newcenter+0.5))
            self.thresholdLine.setValue(newcenter + newvalue)
            self.thresholdLine.viewTransformChanged()
        self._activeIndex = index
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def bumpThresholdUp(self, bump=0.01):
        current = self.thresholdLine.value()
        self.thresholdLine.setValue(current + bump)
        self.thresholdChanged()
    
    def bumpThresholdDown(self, bump=0.01):
        current = self.thresholdLine.value()
        self.thresholdLine.setValue(current - bump)
        self.thresholdChanged()
    
    def thresholdChanged(self):
        trialIndex, muscleIndex = self.muscleTableModel.trialIndex, self._activeIndex
        newvalue = self.thresholdLine.value() - (self.thresholdLine.bounds()[0] + 0.5)
        self.spikeDataModel._params[trialIndex][muscleIndex] = newvalue
    
    def trialSelectionChanged(self, current, previous):
        if isinstance(current, QtCore.QModelIndex):
            index = current.row()
        elif isinstance(current, int):
            index = current
        else:
            raise ValueError("input variable current not a QModelIndex or int")
        self.muscleTableModel.setSelectedIndex(index)
        # Retrieve selected trial's data 
        trial_name = self.trialListModel.trials[index][1]
        fname = os.path.join(self._path_data, trial_name)
        file = scipy.io.loadmat(fname)
        matkeys = [s for s in file.keys()]
        # Grab data, determine which DAQ program was used and cater to file structure of each
        # Newer DAQ program
        if 'data' in matkeys and 'channelNames' in matkeys:
            channelNames = [s[0].lower() for s in file['channelNames'][0]]
            desiredChannelsPresent = [n for n in muscleNamesWithTime if n in channelNames]
            inds = np.array([channelNames.index(n) for n in desiredChannelsPresent])
            datamat = file['data'][:,inds]
        # Old DAQ program
        elif trial_name[0:-4] in matkeys:
            channelNames = [n[0].lower() for n in file[trial_name[0:-4]+'_Header'][0][0][0][0]]
            desiredChannelsPresent = [n for n in muscleNamesWithTime if n in channelNames]
            inds = np.array([channelNames.index(n) for n in desiredChannelsPresent])
            datamat = file[trial_name[0:-4]][:,inds]
        else:
            self.statusBar.showMessage('Cannot open files: These files do not match a format I know.', 3*statusBarDisplayTime)
        self.traceDataModel.setAll(desiredChannelsPresent, datamat)
        # TODO: Put trialListView in congruence with the above and populate off of what's present, rather than what's expected
        # Filter any channels that are already filtered (filtered data not stored, has to be applied when data loaded)
        filtered = np.array([row[2] for row in self.muscleTableModel._data[self.muscleTableModel.trialIndex]])
        names = np.array([sublist[0] for sublist in self.muscleTableModel._data[self.muscleTableModel.trialIndex]])
        if not np.any(filtered):
            self.updateTraceView()
            return
        ti = index
        for ch in names[filtered]:
            mi = muscleNames.index(ch)
            thisfilt = self.spikeDataModel._filters[ti][mi]
            sos = self._filtsos if len(thisfilt) == 0 else thisfilt
            self.filterTrace(ti=ti, mi=mi, sos=sos, changeFlag=False, plotUpdate=False)
        self.updateTraceView()
    
    def muscleSelectionChanged(self):
        self.updateTraceView()
        self.updatePCView()
        self.updateWaveView()
        self.updateSpikeView()
    
    def onFileOpenClick(self):
        # Start one dir back from whatever last data dir was
        startDirGuess = os.path.join(self.settings.value('last_paths', ['~'], str)[0], '..')
        self._path_data = QFileDialog.getExistingDirectory(self, "Open Data Folder", startDirGuess)
        self.initializeDataDir()
    
    def onLoadPreviousClick(self):
        # Get paths, core variables from QSettings, use to populate app
        self._path_data, self._path_amps = self.settings.value('last_paths', [], str)
        self.initializeDataDir()
        
    def onSettingsClick(self):
        self.settingsDialog.exec()
        self.setSettingsCache()
    
    def setSettingsCache(self):
        self.settingsCache = {
            'waveformLength' : int(self.settings.value('waveformLength', '32')),
            'alignAt' : self.settings.value('alignAt', 'local maxima'),
            'deadTime' : int(self.settings.value('deadTime', '10')),
            'fractionPreAlign' : float(self.settings.value('fractionPreAlign', '0.2'))
        }
    
    def initializeDataDir(self):
        self.fileLabel.setText(os.path.basename(self._path_data))
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
            # Generate fresh (muscle, nspike) array
            self.trialListModel.trials = trials
            self.muscleTableModel._data = [[[m, 0, False] for m in muscleNames] for i in range(len(trials))]
            self.spikeDataModel.create(trials, muscleNames, waveformLength=self.settingsCache['waveformLength'])
            self.save()
            self.trialListModel.layoutChanged.emit()
            self.muscleTableModel.layoutChanged.emit()
        # If there is amps dir, load that data
        else: 
            self.load()
    
    def load(self):
        try:
            # Load trial/muscle parameters
            with open(os.path.join(self._path_amps, 'trial_params.json'), 'r') as f:
                data = json.load(f)
                self.trialListModel.trials = data['trialListModel']
                self.muscleTableModel._data = data['muscleTableModel']
                self.trialListModel.layoutChanged.emit()
                self.muscleTableModel.layoutChanged.emit()
            # Load spike data
            muscles = [m[0] for m in self.muscleTableModel._data[0]]
            trials = [t[0] for t in self.trialListModel.trials]
            self.spikeDataModel.create(trials, muscles, waveformLength=self.settingsCache['waveformLength'])
            with open(os.path.join(self._path_amps, 'detection_params.json'), 'r') as f:
                data = json.load(f)
                self.spikeDataModel._params = data['detectFuncParams']
                self.spikeDataModel._filters = [[np.array(arr) for arr in sublist] for sublist in data['filters']]
            with open(os.path.join(self._path_amps, 'detection_functions.pkl'), 'rb') as f:
                self.spikeDataModel._funcs = dill.load(f)
            data = np.genfromtxt(
                os.path.join(self._path_amps, 'spikes.txt'),
                delimiter=','
            )
            # Note: Muscles are numbered in numpy array according to their index/order in muscleTable
            # Assumes every trial for this folder follows same scheme as first trial
            if len(data) != 0:
                for i,trial in enumerate(trials):
                    for j,muscle in enumerate(muscles):
                        self.spikeDataModel.updateSpikes(
                            data[np.logical_and(data[:,0]==int(trial), data[:,1]==j), 2:],
                            (i,j)
                        )
        except Exception:
            pass
    
    def save(self):
        # Don't save if nothing happened
        if len(self.trialListModel.trials) == 0:
            return
        # Otherwise save all main paramters in different files
        with open(os.path.join(self._path_amps, 'trial_params.json'), 'w') as f:
            data = {
                'trialListModel' : self.trialListModel.trials,
                'muscleTableModel' : self.muscleTableModel._data
                }
            json.dump(data, f, indent=4, separators=(',',':'))
        with open(os.path.join(self._path_amps, 'detection_params.json'), 'w') as f:
            data = {
                'detectFuncParams' : self.spikeDataModel._params,
                'filters' : [[arr.tolist() for arr in sublist] for sublist in self.spikeDataModel._filters],
                'sorting date' : str(datetime.datetime.now()),
                'amps version' : 'v0.1'
            }
            json.dump(data, f, indent=4, separators=(',',':'))
        with open(os.path.join(self._path_amps, 'detection_functions.pkl'), 'wb') as f:
            dill.dump(self.spikeDataModel._funcs, f)
        # Put spike numpy arrays together into single array, save
        savelist = []
        for i, perTrialList in enumerate(self.spikeDataModel._spikes):
            trialNum = int(self.trialListModel.trials[i][0])
            for j, arr in enumerate(perTrialList):
                savelist.append(
                    np.concatenate((trialNum * np.ones((arr.shape[0],1)), j * np.ones((arr.shape[0],1)), arr), axis=1)
                )
        savedata = np.vstack(savelist)
        # Create header with column names, muscle numbering scheme
        # Note: Muscles are numbered in numpy array according to their index/order in muscleTable
        # Assumes every trial for this folder follows same scheme as first trial
        colNames = 'trial, muscle, time, unit, valid, prespike, waveform \n'
        muscleScheme = ', '.join([str(i)+' = '+m[0] for (i,m) in enumerate(self.muscleTableModel._data[0])])
        np.savetxt(
            os.path.join(self._path_amps, 'spikes.txt'),
            savedata,
            fmt = ('%u', '%u', '%.18f', '%u', '%u', '%u', *('%.16f' for _ in range(self.settingsCache['waveformLength']))),
            delimiter=',',
            header=colNames + muscleScheme
        )
        self.statusBar.showMessage('file saved', statusBarDisplayTime)
    
    # Execute on app close
    def closeEvent(self, event):
        self.settings.setValue('last_paths', [self._path_data, self._path_amps])
        self.settings.sync()
        self.save()

def mouseDragEvent(ev):
    ev.accept()  # accept all buttons
    dif = (ev.pos() - ev.lastPos()) * -1

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec()