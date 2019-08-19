# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:45:38 2019

Establishes connection with Micro-Manager and Micro Magellan on launch of program

@author: Kyle
"""

from pygellan.acquire import MagellanBridge

def connectMagellan(self):
    self.bridge = MagellanBridge()
    self.core = self.bridge.get_core()
    print('MicroManager Socket:')
    print(self.core.socket)
    self.magellan = self.bridge.get_magellan()
    print('MicroMagellan Socket:')
    print(self.magellan.socket)
