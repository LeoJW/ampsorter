import numpy as np
from scipy.signal import sosfiltfilt
from PyQt6 import QtCore
from PyQt6.QtGui import QColor


filtEnableColor = '#73A843'

class SpikeDataModel():
    def create(self, trials, muscles, paramDefault=0.4, waveformLength=32):
        # Assumes every trial has the same muscles
        # Spikes columns were in v0.2 [time, unit, valid, samples pre-spike, waveform...]
        # Spikes columns are [time, sample, unit, valid, samples pre-spike, waveform...]
        self._spikes = [[np.empty((0, 5 + waveformLength)) for _ in muscles] for _ in trials]
        self._params = [[paramDefault for _ in muscles] for _ in trials]
        self._funcs = [[lambda t,a: a for _ in muscles] for _ in trials]
        self._pc = [[np.empty((0, 2)) for _ in muscles] for _ in trials]
        self._filters = [[np.empty((0,0)) for _ in muscles] for _ in trials]
    def updateSpikes(self, data, index):
        self._spikes[index[0]][index[1]] = data
    def updatePCA(self, index):
        # Note that PCA here is effectively done using correlation matrix 
        # (each variable divided by standard deviation), not covariance matrix
        if self._spikes[index[0]][index[1]].shape[0] <= 1:
            self._pc[index[0]][index[1]] = np.empty((0, 2))
            return
        x = np.copy(self._spikes[index[0]][index[1]][:,5:])
        x -= np.mean(x, axis=0)
        x /= np.std(x, axis=0)
        cov = np.cov(x, rowvar=False, bias=True)
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argsort(eigvals)[::-1]
        eigvecs = eigvecs[:,idx]
        eigvals = eigvals[idx]
        scores = np.dot(x, eigvecs)
        self._pc[index[0]][index[1]] = scores[:,:]


class TraceDataModel():
    def __init__(self, channelNames=[''], matrix=np.zeros((1,1)), *args, **kwargs):
        self.setAll(channelNames, matrix)
        self._replaceMuscles = {}
    
    def setAll(self, channelNames, matrix):
        self._names = channelNames
        # Identify dimension of matrix that matches length of names
        if len(self._names) in matrix.shape:
            # Arrange so channel dimension always on rows
            if matrix.shape.index(len(self._names)) == 1:
                matrix = matrix.T
        else:
            raise ValueError(f"Gave {len(self._names)} names but data matrix has no matching dimension")
        # Store two copies of the data: an original master, and processed form
        self._maindata = {}
        self._filtdata = {}
        for i,n in enumerate(self._names):
            self._maindata[n] = matrix[i,:].reshape(-1)
            self._filtdata[n] = matrix[i,:].reshape(-1)
        self.normalize()
        # If no time channel, make fake one
        if 'time' not in self._names:
            self._maindata['time'] = np.arange(matrix.shape[1])
            self._filtdata['time'] = np.arange(matrix.shape[1])
        # Save sample rate. Use 1 if there's basically no data
        if len(self._maindata['time']) >= 10:
            self._fs = 1 / np.mean(np.diff(self._maindata['time'][0:10]))
        else:
            self._fs = 1.0
    def setReplace(self, source, target):
        if source not in self._names or target not in self._names:
            return
        self._replaceMuscles[target] = source
        self._filtdata[target] = self._maindata[source]
    def clearReplace(self, target):
        self._filtdata[target] = self._maindata[target]
        self._replaceMuscles = {}
    def get(self, name):
        # Always return processed form, even if no processing
        return self._filtdata[name]
    def normalize(self, name=None):
        # Do all if no specific specified (except time!)
        if name == None:
            name = [n for n in self._names if 'time' not in n.lower()]
        # If only one specified make list
        elif isinstance(name, str): 
            name = [name]
        # Run normalization on all specified
        for n in name:
            max, min = self._filtdata[n].max(), self._filtdata[n].min()
            if max != min:
                self._filtdata[n] /= (max - min)
    def rescale(self, factor=1):
        for n in self._names:
            self._filtdata[n] *= factor
    def filter(self, name, filtsos):
        if isinstance(name, str):
            name = [name]
        for n in name:
            self._filtdata[n] = sosfiltfilt(filtsos, self._filtdata[n])
    def restore(self, name):
        if isinstance(name, str):
            name = [name]
        for n in name:
            if n in self._replaceMuscles.keys():
                self._filtdata[n] = self._maindata[self._replaceMuscles[n]]
            else:
                self._filtdata[n] = self._maindata[n]


class TrialListModel(QtCore.QAbstractListModel):
    def __init__(self, trials=None, *args, **kwargs):
        super(TrialListModel, self). __init__(*args, **kwargs)
        self.trials = trials or []
    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            trial_num, trial_name = self.trials[index.row()]
            return trial_num
    def rowCount(self, index):
        return len(self.trials)


class MuscleTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[[]]]):
        super(MuscleTableModel, self).__init__()
        self._data = data
        self.trialIndex = 0
    def setSelectedIndex(self, index):
        self.trialIndex = index
        self.layoutChanged.emit()
    def rowCount(self, index):
        # The length of the outer list
        return len(self._data[self.trialIndex])
    def columnCount(self, index):
        # Takes first sub-list of first trial, returns length
        # (only works if all rows are an equal length)
        return len(self._data[0][0]) 
    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            value = self._data[self.trialIndex][index.row()][index.column()]
            if isinstance(value, bool):
                value = None
            return value
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            value = self._data[self.trialIndex][index.row()][index.column()]
            if isinstance(value, bool) and value:
                return QColor(filtEnableColor)