# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SlideROIs.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(934, 713)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.slideROIs_graphicsView = ImageView(self.centralwidget)
        self.slideROIs_graphicsView.setGeometry(QtCore.QRect(40, 20, 861, 581))
        self.slideROIs_graphicsView.setObjectName("slideROIs_graphicsView")
        self.close_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.close_pushButton.setGeometry(QtCore.QRect(430, 610, 121, 51))
        self.close_pushButton.setObjectName("close_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 934, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.close_pushButton.setText(_translate("MainWindow", "Close"))

from pyqtgraph import ImageView
