import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore


class RectSelectViewBox(pg.ViewBox):
    sigSelectionReleased = QtCore.Signal(object)
    
    def __init__(self):
        super().__init__()
        self.pressedKey = ''
        self.rectCoords = ()
    
    def mouseDragEvent(self, ev, axis=None):
        ev.accept()  ## we accept all buttons
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1
        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float64)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1-axis] = 0.0
        ## Scale or translate based on mouse button
        if ev.button() in [QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.MiddleButton]:
            if self.state['mouseMode'] == pg.ViewBox.RectMode and axis is None:
                if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                    self.rbScaleBox.hide()
                    ax = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                    ax = self.childGroup.mapRectFromParent(ax)
                    self.rectCoords =  ax.getCoords() 
                    self.sigSelectionReleased.emit(self)
                    self.pressedKey = None
                else:
                    ## update shape of scale box
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())
        elif ev.button() & QtCore.Qt.MouseButton.RightButton:
            if self.state['aspectLocked'] is not False:
                mask[0] = 0
            dif = ev.screenPos() - ev.lastScreenPos()
            dif = np.array([dif.x(), dif.y()])
            dif[0] *= -1
            s = ((mask * 0.02) + 1) ** dif
            tr = self.childGroup.transform()
            tr = pg.functions.invertQTransform(tr)
            x = s[0] if mouseEnabled[0] == 1 else None
            y = s[1] if mouseEnabled[1] == 1 else None
            center = pg.Point(tr.map(ev.buttonDownPos(QtCore.Qt.MouseButton.RightButton)))
            self._resetTarget()
            self.scaleBy(x=x, y=y, center=center)
            self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
    
    def keyPressEvent(self, ev):
        ev.accept()
        if not ev.isAutoRepeat():
            self.pressedKey = ev.text()

class RectSelectPlotWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super(RectSelectPlotWidget, self).__init__(parent, viewBox=RectSelectViewBox())

# PolyLineROI; make new point if mouse location X distance from last point
