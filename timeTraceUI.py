# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timeTracker3.ui'
#
# Created: Fri Jan 03 10:53:21 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!
# customized from pyside-uic source

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(40, 50, 311, 121))
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.setObjectName("lcdNumber")
        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(150, 190, 93, 28))
        self.stop.setObjectName("stop")
        self.exit = QtGui.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(260, 190, 93, 28))
        self.exit.setObjectName("exit")
        self.start = QtGui.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(40, 190, 93, 28))
        self.start.setObjectName("start")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 406, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.stop.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.exit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.start.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))

