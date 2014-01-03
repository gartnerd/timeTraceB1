# -*- coding: utf-8 -*-
#files for beta test 1 - time tracker
import sys
import time
import datetime

from PySide import QtCore, QtGui
from timeTraceUI import Ui_MainWindow


class timers(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(timers, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lcdTimer = QtCore.QTimer()
        self.lcdElapsedTimer = QtCore.QElapsedTimer()

        #buttons
        QtCore.QObject.connect(self.ui.exit, QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QObject.connect(self.ui.stop, QtCore.SIGNAL("clicked()"), self.stop_clock)
        QtCore.QObject.connect(self.ui.start, QtCore.SIGNAL("clicked()"), self.start_clock)

        QtCore.QObject.connect(self.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime)

        QtCore.QMetaObject.connectSlotsByName(self)

    def constant(self):
        """
        Start the constant timer
        """
        self.ctimer.start(1000)

    def start_clock(self):
        self.lcdElapsedTimer.start()
        self.lcdTimer.start(1000)

    def stop_clock(self):
        self.lcdTimer.stop()

    def constantUpdate(self):
        """
        slot for constant timer timeout
        """
        pass

    def single(self):
        """
        run singleShot timer after button push
        """
        self.stimer.singleShot(1000, self.singleUpdate)

    def singleUpdate(self):
        """
        Slot for singleShot timer timeout
        """
        pass

    def updtTime(self):
        #currentTime = QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')
        currentTime = datetime.timedelta(seconds=self.lcdElapsedTimer.elapsed()/1000)
        self.ui.lcdNumber.display(str(currentTime))
        #self.ui.myTimeDisplay.display(currentTime)
        #print currentTime

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = timers()
    myapp.show()
    sys.exit(app.exec_())
