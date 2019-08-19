# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:05:34 2019

@author: Kyle

Main window of the GUI. Talks with all of the other models and controllers to
dispay the image and quantitative data.
"""

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPixmap

from mainGUI_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self):
        
        super().__init__() 
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        
       