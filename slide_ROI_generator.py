# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:19:44 2019

@author: Kyle
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from mainGUI import MainView
import createBridge


class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        
        self.main_view = MainView()
        self.main_view.show()
        createBridge.connectMagellan(self)
        
if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())