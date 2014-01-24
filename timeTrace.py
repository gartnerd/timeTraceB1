# -*- coding: utf-8 -*-
#files for beta test 1 - time tracker
import sys
import time
import datetime
import connection

from PySide import QtCore, QtGui, QtSql
from timeTraceUI import Ui_MainWindow
from taskpopup import SortedDict, ChargeCodeCatalog


class timers(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(timers, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tl = ChargeCodeCatalog()

        #self.c2 = 0
        #currentTime2 = 0

        self.clock1 = StartStopClock()
        self.clock2 = StartStopClock()
        self.clock3 = StartStopClock()

        self.lcdTime = QtCore.QTimer()
        self.lcdTime.start(1000)

        #self.deltatime = self.clock1.lcdElapsedTimer.elapsed()
        #self.clock1delta = ElapsedTime()
        #self.clock1delta.elapsedTime(self.deltatime)

        #buttons
        QtCore.QObject.connect(self.ui.stop,    QtCore.SIGNAL("clicked()"), self.clock1.stop_clock)
        QtCore.QObject.connect(self.ui.stop,    QtCore.SIGNAL("clicked()"), self.clock3.stop_clock)
        QtCore.QObject.connect(self.ui.start,   QtCore.SIGNAL("clicked()"), self.clock1.start_clock)
        QtCore.QObject.connect(self.ui.start,   QtCore.SIGNAL("clicked()"), self.clock3.start_clock)
        QtCore.QObject.connect(self.ui.stop_2,  QtCore.SIGNAL("clicked()"), self.clock2.stop_clock)
        QtCore.QObject.connect(self.ui.stop_2,  QtCore.SIGNAL("clicked()"), self.clock3.start_clock)
        QtCore.QObject.connect(self.ui.start_2, QtCore.SIGNAL("clicked()"), self.clock2.start_clock)
        QtCore.QObject.connect(self.ui.start_2, QtCore.SIGNAL("clicked()"), self.clock3.stop_clock)
        QtCore.QObject.connect(self.ui.stop_3,  QtCore.SIGNAL("clicked()"), self.clock3.stop_clock)
        QtCore.QObject.connect(self.ui.start_3, QtCore.SIGNAL("clicked()"), self.clock3.start_clock)
        QtCore.QObject.connect(self.ui.start_3, QtCore.SIGNAL("clicked()"), self.clock2.stop_clock)
        QtCore.QObject.connect(self.ui.actionSelect_Task, QtCore.SIGNAL("triggered()"), self.tl.show)

        QtCore.QObject.connect(self.clock1.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime)
        QtCore.QObject.connect(self.clock2.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime2)
        QtCore.QObject.connect(self.clock3.lcdTimer, QtCore.SIGNAL("timeout()"), self.updtTime3)
        QtCore.QObject.connect(self.lcdTime, QtCore.SIGNAL("timeout()"), self.updtTime4)

        QtCore.QMetaObject.connectSlotsByName(self)

    def select_task(self):
        self.tl.show()

    def single(self):
        """
        run singleShot timer after button push
        """
        self.stimer.singleShot(1000, self.singleUpdate)

    def updtTime(self):
        currentTime1 = datetime.timedelta(seconds=self.clock1.lcdElapsedTimer.elapsed()/1000)
        self.ui.lcdNumber.display(str(currentTime1))

    def updtTime2(self):
        if self.clock2.c2 == 0:
            currentTime2 = datetime.timedelta(seconds=self.clock2.lcdElapsedTimer.elapsed()/1000)
        else:
            currentTime2 = datetime.timedelta(seconds=(self.clock2.lcdElapsedTimer.elapsed() + sum(self.clock2.timelist))/1000)

        self.ui.lcdNumber_2.display(str(currentTime2))

    def updtTime3(self):
        if self.clock3.c2 == 0:
            currentTime3 = datetime.timedelta(seconds=self.clock3.lcdElapsedTimer.elapsed()/1000)
        else:
            currentTime3 = datetime.timedelta(seconds=(self.clock3.lcdElapsedTimer.elapsed() + sum(self.clock3.timelist))/1000)

        self.ui.lcdNumber_3.display(str(currentTime3))

    def updtTime4(self):
        currentTime = QtCore.QDateTime.currentDateTime().toString('hh:mm')
        self.ui.lcdNumber_4.display(str(currentTime))

class ElapsedTime(object):
    def elapsedTime(self,deltaTime):
        self.delT = datetime.timedelta(seconds=deltaTime)
        #return self.delT
        #self.lcdDisplay.display(str(self.delT))


class StartStopClock(object):
    def __init__(self):
        self.lcdTimer = QtCore.QTimer()
        self.lcdElapsedTimer = QtCore.QElapsedTimer()
        self.c2 = 0
        self.timelist = []

    def start_clock(self):
        self.lcdElapsedTimer.start()
        self.lcdTimer.start(1000)

    def stop_clock(self):
        self.c2 = 1
        self.timelist.append(self.lcdElapsedTimer.elapsed())
        self.lcdTimer.stop()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    model = QtSql.QSqlTableModel()
    connection.initializeModel(model)

    view1 = connection.createView("Charge Code Table Model", model)
    view1.show()

    myapp = timers()
    myapp.show()
    sys.exit(app.exec_())

#PySide.QtSql.QSqlTableModel.insertRecord(row, record) record is a QSqlRecord thing
#PySide.QtSql.QSqlRecord(other)