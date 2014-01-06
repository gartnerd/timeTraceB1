# -*- coding: utf-8 -*-
#files for beta test 1 - time tracker
import sys
import time
import datetime

from PySide import QtCore, QtGui
from timeTraceUI2 import Ui_MainWindow


class timers(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(timers, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.clock1 = StartStopClock()
        self.deltatime = self.clock1.lcdElapsedTimer.elapsed()
        self.clock1delta = ElapsedTime()
        self.clock1delta.elapsedTime(self.deltatime)

        self.clock2 = StartStopClock()

        #buttons
        QtCore.QObject.connect(self.ui.exit,    QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QObject.connect(self.ui.exit_2,  QtCore.SIGNAL("clicked()"), self.close)
        QtCore.QObject.connect(self.ui.stop,    QtCore.SIGNAL("clicked()"), self.clock1.stop_clock)
        QtCore.QObject.connect(self.ui.start,   QtCore.SIGNAL("clicked()"), self.clock1.start_clock)
        QtCore.QObject.connect(self.ui.stop_2,  QtCore.SIGNAL("clicked()"), self.clock2.stop_clock)
        QtCore.QObject.connect(self.ui.start_2, QtCore.SIGNAL("clicked()"), self.clock2.start_clock)

        QtCore.QObject.connect(self.clock1.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime)
        QtCore.QObject.connect(self.clock2.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime2)


        QtCore.QMetaObject.connectSlotsByName(self)


    def single(self):
        """
        run singleShot timer after button push
        """
        self.stimer.singleShot(1000, self.singleUpdate)


    def updtTime(self):
        currentTime1 = datetime.timedelta(seconds=self.clock1.lcdElapsedTimer.elapsed()/1000)
        self.ui.lcdNumber.display(str(currentTime1))

    def updtTime2(self):
        #currentTime = QtCore.QDateTime.currentDateTime().toString('hh:mm:ss')
        currentTime2 = datetime.timedelta(seconds=self.clock2.lcdElapsedTimer.elapsed()/1000)
        self.ui.lcdNumber_2.display(str(currentTime2))

class ElapsedTime(object):
    def elapsedTime(self,deltaTime):
        self.delT = datetime.timedelta(seconds=deltaTime)
        #return self.delT
        #self.lcdDisplay.display(str(self.delT))


class StartStopClock(object):
    def __init__(self):
        self.lcdTimer = QtCore.QTimer()
        self.lcdElapsedTimer = QtCore.QElapsedTimer()

    def start_clock(self):
        self.lcdElapsedTimer.start()
        self.lcdTimer.start(1000)

    def stop_clock(self):
        self.lcdTimer.stop()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = timers()
    myapp.show()
    sys.exit(app.exec_())
