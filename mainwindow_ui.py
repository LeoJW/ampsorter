# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(976, 673)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.widget = QtWidgets.QWidget(parent=MainWindow)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.muscleView = QtWidgets.QTableView(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.muscleView.sizePolicy().hasHeightForWidth())
        self.muscleView.setSizePolicy(sizePolicy)
        self.muscleView.setMinimumSize(QtCore.QSize(0, 260))
        self.muscleView.setMaximumSize(QtCore.QSize(140, 400))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.muscleView.setFont(font)
        self.muscleView.setAlternatingRowColors(True)
        self.muscleView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.muscleView.setObjectName("muscleView")
        self.muscleView.horizontalHeader().setVisible(False)
        self.muscleView.verticalHeader().setVisible(False)
        self.muscleView.verticalHeader().setDefaultSectionSize(7)
        self.muscleView.verticalHeader().setMinimumSectionSize(5)
        self.gridLayout.addWidget(self.muscleView, 0, 2, 1, 1)
        self.trialView = QtWidgets.QListView(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialView.sizePolicy().hasHeightForWidth())
        self.trialView.setSizePolicy(sizePolicy)
        self.trialView.setMinimumSize(QtCore.QSize(0, 260))
        self.trialView.setMaximumSize(QtCore.QSize(50, 400))
        self.trialView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.trialView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.trialView.setObjectName("trialView")
        self.gridLayout.addWidget(self.trialView, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 7, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(210, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 400))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabDetect = QtWidgets.QWidget()
        self.tabDetect.setObjectName("tabDetect")
        self.detectSpikesButton = QtWidgets.QPushButton(parent=self.tabDetect)
        self.detectSpikesButton.setGeometry(QtCore.QRect(0, 180, 127, 32))
        self.detectSpikesButton.setObjectName("detectSpikesButton")
        self.undetectSpikesButton = QtWidgets.QPushButton(parent=self.tabDetect)
        self.undetectSpikesButton.setGeometry(QtCore.QRect(120, 180, 81, 32))
        self.undetectSpikesButton.setObjectName("undetectSpikesButton")
        self.autosetThresholdsButton = QtWidgets.QPushButton(parent=self.tabDetect)
        self.autosetThresholdsButton.setGeometry(QtCore.QRect(0, 20, 141, 32))
        self.autosetThresholdsButton.setObjectName("autosetThresholdsButton")
        self.autodetectButton = QtWidgets.QPushButton(parent=self.tabDetect)
        self.autodetectButton.setGeometry(QtCore.QRect(0, 50, 141, 32))
        self.autodetectButton.setObjectName("autodetectButton")
        self.label = QtWidgets.QLabel(parent=self.tabDetect)
        self.label.setGeometry(QtCore.QRect(10, 160, 121, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.tabDetect)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 191, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.autoApplyFiltersRadioButton = QtWidgets.QRadioButton(parent=self.tabDetect)
        self.autoApplyFiltersRadioButton.setGeometry(QtCore.QRect(10, 80, 181, 20))
        self.autoApplyFiltersRadioButton.setChecked(True)
        self.autoApplyFiltersRadioButton.setObjectName("autoApplyFiltersRadioButton")
        self.tabWidget.addTab(self.tabDetect, "")
        self.tabUnits = QtWidgets.QWidget()
        self.tabUnits.setObjectName("tabUnits")
        self.invalidateCrosstalkButton = QtWidgets.QPushButton(parent=self.tabUnits)
        self.invalidateCrosstalkButton.setGeometry(QtCore.QRect(0, 0, 151, 31))
        self.invalidateCrosstalkButton.setObjectName("invalidateCrosstalkButton")
        self.crosstalkMuscleLineEdit = QtWidgets.QLineEdit(parent=self.tabUnits)
        self.crosstalkMuscleLineEdit.setGeometry(QtCore.QRect(70, 30, 51, 21))
        self.crosstalkMuscleLineEdit.setObjectName("crosstalkMuscleLineEdit")
        self.label_4 = QtWidgets.QLabel(parent=self.tabUnits)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 51, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.tabUnits)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_5.setObjectName("label_5")
        self.crosstalkWindowLineEdit = QtWidgets.QLineEdit(parent=self.tabUnits)
        self.crosstalkWindowLineEdit.setGeometry(QtCore.QRect(70, 50, 51, 21))
        self.crosstalkWindowLineEdit.setObjectName("crosstalkWindowLineEdit")
        self.label_6 = QtWidgets.QLabel(parent=self.tabUnits)
        self.label_6.setGeometry(QtCore.QRect(120, 50, 31, 16))
        self.label_6.setObjectName("label_6")
        self.invalidateUnitButton = QtWidgets.QPushButton(parent=self.tabUnits)
        self.invalidateUnitButton.setGeometry(QtCore.QRect(0, 80, 151, 31))
        self.invalidateUnitButton.setObjectName("invalidateUnitButton")
        self.invalidateUnitLineEdit = QtWidgets.QLineEdit(parent=self.tabUnits)
        self.invalidateUnitLineEdit.setGeometry(QtCore.QRect(70, 110, 51, 21))
        self.invalidateUnitLineEdit.setObjectName("invalidateUnitLineEdit")
        self.label_7 = QtWidgets.QLabel(parent=self.tabUnits)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 51, 16))
        self.label_7.setObjectName("label_7")
        self.reassignButton = QtWidgets.QPushButton(parent=self.tabUnits)
        self.reassignButton.setGeometry(QtCore.QRect(0, 150, 151, 31))
        self.reassignButton.setObjectName("reassignButton")
        self.reassignSourceLineEdit = QtWidgets.QLineEdit(parent=self.tabUnits)
        self.reassignSourceLineEdit.setGeometry(QtCore.QRect(120, 180, 51, 21))
        self.reassignSourceLineEdit.setObjectName("reassignSourceLineEdit")
        self.reassignTargetLineEdit = QtWidgets.QLineEdit(parent=self.tabUnits)
        self.reassignTargetLineEdit.setGeometry(QtCore.QRect(10, 180, 51, 21))
        self.reassignTargetLineEdit.setObjectName("reassignTargetLineEdit")
        self.label_8 = QtWidgets.QLabel(parent=self.tabUnits)
        self.label_8.setGeometry(QtCore.QRect(60, 180, 61, 21))
        self.label_8.setObjectName("label_8")
        self.clearReassignmentsButton = QtWidgets.QPushButton(parent=self.tabUnits)
        self.clearReassignmentsButton.setGeometry(QtCore.QRect(0, 200, 151, 31))
        self.clearReassignmentsButton.setObjectName("clearReassignmentsButton")
        self.line = QtWidgets.QFrame(parent=self.tabUnits)
        self.line.setGeometry(QtCore.QRect(0, 70, 201, 16))
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(parent=self.tabUnits)
        self.line_2.setGeometry(QtCore.QRect(0, 130, 201, 16))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setObjectName("line_2")
        self.tabWidget.addTab(self.tabUnits, "")
        self.tabFilter = QtWidgets.QWidget()
        self.tabFilter.setObjectName("tabFilter")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.tabFilter)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 201, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapLongRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.passTypeLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passTypeLabel.setFont(font)
        self.passTypeLabel.setObjectName("passTypeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.passTypeLabel)
        self.passTypeComboBox = QtWidgets.QComboBox(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passTypeComboBox.setFont(font)
        self.passTypeComboBox.setFrame(True)
        self.passTypeComboBox.setObjectName("passTypeComboBox")
        self.passTypeComboBox.addItem("")
        self.passTypeComboBox.addItem("")
        self.passTypeComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.passTypeComboBox)
        self.filterTypeLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.filterTypeLabel.setFont(font)
        self.filterTypeLabel.setObjectName("filterTypeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.filterTypeLabel)
        self.filterTypeComboBox = QtWidgets.QComboBox(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.filterTypeComboBox.setFont(font)
        self.filterTypeComboBox.setObjectName("filterTypeComboBox")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.filterTypeComboBox)
        self.highpassCutoffHzLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.highpassCutoffHzLabel.setFont(font)
        self.highpassCutoffHzLabel.setObjectName("highpassCutoffHzLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.highpassCutoffHzLabel)
        self.highpassCutoffHzLineEdit = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.highpassCutoffHzLineEdit.setFont(font)
        self.highpassCutoffHzLineEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.highpassCutoffHzLineEdit.setObjectName("highpassCutoffHzLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.highpassCutoffHzLineEdit)
        self.lowpassCutoffHzLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lowpassCutoffHzLabel.setFont(font)
        self.lowpassCutoffHzLabel.setObjectName("lowpassCutoffHzLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lowpassCutoffHzLabel)
        self.lowpassCutoffHzLineEdit = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lowpassCutoffHzLineEdit.setFont(font)
        self.lowpassCutoffHzLineEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.lowpassCutoffHzLineEdit.setObjectName("lowpassCutoffHzLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.lowpassCutoffHzLineEdit)
        self.orderLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.orderLabel.setFont(font)
        self.orderLabel.setObjectName("orderLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.orderLabel)
        self.orderLineEdit = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.orderLineEdit.setFont(font)
        self.orderLineEdit.setObjectName("orderLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.orderLineEdit)
        self.passbandRippleDBLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passbandRippleDBLabel.setFont(font)
        self.passbandRippleDBLabel.setObjectName("passbandRippleDBLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.passbandRippleDBLabel)
        self.passbandRippleDBLineEdit = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passbandRippleDBLineEdit.setFont(font)
        self.passbandRippleDBLineEdit.setObjectName("passbandRippleDBLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.passbandRippleDBLineEdit)
        self.stopbandAttenDBLabel = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stopbandAttenDBLabel.setFont(font)
        self.stopbandAttenDBLabel.setObjectName("stopbandAttenDBLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.stopbandAttenDBLabel)
        self.stopbandAttenDBLineEdit = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stopbandAttenDBLineEdit.setFont(font)
        self.stopbandAttenDBLineEdit.setObjectName("stopbandAttenDBLineEdit")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.stopbandAttenDBLineEdit)
        self.freqResponseView = PlotWidget(parent=self.tabFilter)
        self.freqResponseView.setGeometry(QtCore.QRect(0, 190, 201, 51))
        self.freqResponseView.setObjectName("freqResponseView")
        self.tabWidget.addTab(self.tabFilter, "")
        self.tabPCA = QtWidgets.QWidget()
        self.tabPCA.setObjectName("tabPCA")
        self.pcaXValueInput = QtWidgets.QLineEdit(parent=self.tabPCA)
        self.pcaXValueInput.setGeometry(QtCore.QRect(10, 10, 81, 22))
        self.pcaXValueInput.setText("")
        self.pcaXValueInput.setObjectName("pcaXValueInput")
        self.pcaYValueInput = QtWidgets.QLineEdit(parent=self.tabPCA)
        self.pcaYValueInput.setGeometry(QtCore.QRect(10, 30, 81, 22))
        self.pcaYValueInput.setText("")
        self.pcaYValueInput.setObjectName("pcaYValueInput")
        self.tabWidget.addTab(self.tabPCA, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 3, 1, 2)
        self.spikeView = RectSelectPlotWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spikeView.sizePolicy().hasHeightForWidth())
        self.spikeView.setSizePolicy(sizePolicy)
        self.spikeView.setMinimumSize(QtCore.QSize(0, 10))
        self.spikeView.setBaseSize(QtCore.QSize(0, 0))
        self.spikeView.setObjectName("spikeView")
        self.gridLayout.addWidget(self.spikeView, 2, 1, 1, 7)
        self.traceView = PlotWidget(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.traceView.sizePolicy().hasHeightForWidth())
        self.traceView.setSizePolicy(sizePolicy)
        self.traceView.setObjectName("traceView")
        self.gridLayout.addWidget(self.traceView, 1, 1, 1, 7)
        self.pcView = RectSelectPlotWidget(parent=self.widget)
        self.pcView.setMaximumSize(QtCore.QSize(16777215, 400))
        self.pcView.setObjectName("pcView")
        self.gridLayout.addWidget(self.pcView, 0, 6, 1, 1)
        self.waveView = PlotWidget(parent=self.widget)
        self.waveView.setMaximumSize(QtCore.QSize(16777215, 400))
        self.waveView.setObjectName("waveView")
        self.gridLayout.addWidget(self.waveView, 0, 5, 1, 1)
        MainWindow.setCentralWidget(self.widget)
        self.statusBar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Assisted Motor Program Sorter (AMPS)"))
        self.detectSpikesButton.setText(_translate("MainWindow", "Detect Spikes"))
        self.undetectSpikesButton.setText(_translate("MainWindow", "Undetect"))
        self.autosetThresholdsButton.setText(_translate("MainWindow", "Autoset Thesholds"))
        self.autodetectButton.setText(_translate("MainWindow", "Autodetect"))
        self.label.setText(_translate("MainWindow", "For selected trace:"))
        self.label_2.setText(_translate("MainWindow", "Based on all detected so far:"))
        self.autoApplyFiltersRadioButton.setText(_translate("MainWindow", "apply filters automatically"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDetect), _translate("MainWindow", "Detection"))
        self.invalidateCrosstalkButton.setText(_translate("MainWindow", "Invalidate crosstalk"))
        self.crosstalkMuscleLineEdit.setText(_translate("MainWindow", "lax"))
        self.label_4.setText(_translate("MainWindow", "Muscle:"))
        self.label_5.setText(_translate("MainWindow", "Window:"))
        self.crosstalkWindowLineEdit.setText(_translate("MainWindow", "3"))
        self.label_6.setText(_translate("MainWindow", "(ms)"))
        self.invalidateUnitButton.setText(_translate("MainWindow", "Invalidate all in unit"))
        self.invalidateUnitLineEdit.setText(_translate("MainWindow", "1"))
        self.label_7.setText(_translate("MainWindow", "Unit:"))
        self.reassignButton.setText(_translate("MainWindow", "Reassign X to Y"))
        self.reassignSourceLineEdit.setText(_translate("MainWindow", "lba"))
        self.reassignTargetLineEdit.setText(_translate("MainWindow", "lax"))
        self.label_8.setText(_translate("MainWindow", "becomes"))
        self.clearReassignmentsButton.setText(_translate("MainWindow", "Clear reassignments"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabUnits), _translate("MainWindow", "Units"))
        self.passTypeLabel.setText(_translate("MainWindow", "Pass Type"))
        self.passTypeComboBox.setItemText(0, _translate("MainWindow", "highpass"))
        self.passTypeComboBox.setItemText(1, _translate("MainWindow", "bandpass"))
        self.passTypeComboBox.setItemText(2, _translate("MainWindow", "lowpass"))
        self.filterTypeLabel.setText(_translate("MainWindow", "Filter Type"))
        self.filterTypeComboBox.setToolTip(_translate("MainWindow", "<html><head/><body><p>butterworth - maximally flat frequency response</p><p>chebyshev1 - Approx. of ideal response, with passband ripple</p><p>chebyshev2 - Approx. of ideal response, with stopband ripple</p><p>elliptic - Steepest cutoff, variable ripple in each band</p></body></html>"))
        self.filterTypeComboBox.setItemText(0, _translate("MainWindow", "butterworth"))
        self.filterTypeComboBox.setItemText(1, _translate("MainWindow", "chebyshev1"))
        self.filterTypeComboBox.setItemText(2, _translate("MainWindow", "chebyshev2"))
        self.filterTypeComboBox.setItemText(3, _translate("MainWindow", "elliptic"))
        self.highpassCutoffHzLabel.setText(_translate("MainWindow", "Highpass Cutoff (Hz)"))
        self.highpassCutoffHzLineEdit.setText(_translate("MainWindow", "100"))
        self.lowpassCutoffHzLabel.setText(_translate("MainWindow", "Lowpass Cutoff (Hz)"))
        self.lowpassCutoffHzLineEdit.setText(_translate("MainWindow", "500"))
        self.orderLabel.setText(_translate("MainWindow", "Order"))
        self.orderLineEdit.setText(_translate("MainWindow", "4"))
        self.passbandRippleDBLabel.setText(_translate("MainWindow", "Passband Ripple (dB)"))
        self.passbandRippleDBLineEdit.setText(_translate("MainWindow", "5"))
        self.stopbandAttenDBLabel.setText(_translate("MainWindow", "Stopband Atten. (dB)"))
        self.stopbandAttenDBLineEdit.setText(_translate("MainWindow", "50"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilter), _translate("MainWindow", "Filters"))
        self.pcaXValueInput.setPlaceholderText(_translate("MainWindow", "PC x-value"))
        self.pcaYValueInput.setPlaceholderText(_translate("MainWindow", "PC y-value"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPCA), _translate("MainWindow", "PC"))
from pyqtgraph import PlotWidget
from selectplotwidget import RectSelectPlotWidget
