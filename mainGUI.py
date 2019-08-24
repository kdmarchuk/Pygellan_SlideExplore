# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:05:34 2019

@author: Kyle

Main window of the GUI. 
"""

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt, QRectF
from PyQt5.QtGui import QPixmap

import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg

from mainGUI_ui import Ui_MainWindow

import createBridge


class MainView(QMainWindow):
    def __init__(self):
        
        super().__init__() 
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.connx = createBridge.Connection()
        
    
        ### Connections for Days
        # Image Push Buttons
        self._ui.snapTop_pushButton.clicked.connect(self.pressSnapTop)
        self._ui.snapBottom_pushButton.clicked.connect(self.pressSnapBottom)
        self._ui.snapLeft_pushButton.clicked.connect(self.pressSnapLeft)
        self._ui.snapRight_pushButton.clicked.connect(self.pressSnapRight)

        # Turn off default pyqtgraph visualization settings
        # Top Image
        self._ui.topImage_graphicsView.ui.histogram.hide()
        self._ui.topImage_graphicsView.ui.roiBtn.hide()
        self._ui.topImage_graphicsView.ui.menuBtn.hide()
        self._ui.topImage_graphicsView.view.setAspectLocked()
        self._ui.topImage_graphicsView.view.invertX()

        self.roiTop = pg.LineSegmentROI([[10, 128],[492,128]],maxBounds=QRectF(0,0,512,512),pen='r')
        self._ui.topImage_graphicsView.view.addItem(self.roiTop)
        self.roiTop.sigRegionChangeFinished.connect(self.updateTop)
        # Bottom Image
        self._ui.bottomImage_graphicsView.ui.histogram.hide()
        self._ui.bottomImage_graphicsView.ui.roiBtn.hide()
        self._ui.bottomImage_graphicsView.ui.menuBtn.hide()
        self._ui.bottomImage_graphicsView.view.setAspectLocked()
        self._ui.bottomImage_graphicsView.view.invertX()

        self.roiBottom = pg.LineSegmentROI([[10, 128],[492,128]],maxBounds=QRectF(0,0,512,512),pen='b')
        self._ui.bottomImage_graphicsView.view.addItem(self.roiBottom)
        self.roiBottom.sigRegionChangeFinished.connect(self.updateBottom)
        # Left Image
        self._ui.leftImage_graphicsView.ui.histogram.hide()
        self._ui.leftImage_graphicsView.ui.roiBtn.hide()
        self._ui.leftImage_graphicsView.ui.menuBtn.hide()
        self._ui.leftImage_graphicsView.view.setAspectLocked()
        self._ui.leftImage_graphicsView.view.invertX()

        self.roiLeft = pg.LineSegmentROI([[10, 128],[492,128]],maxBounds=QRectF(0,0,512,512),pen='g')
        self._ui.leftImage_graphicsView.view.addItem(self.roiLeft)
        self.roiLeft.sigRegionChangeFinished.connect(self.updateLeft)
        # right Image
        self._ui.rightImage_graphicsView.ui.histogram.hide()
        self._ui.rightImage_graphicsView.ui.roiBtn.hide()
        self._ui.rightImage_graphicsView.ui.menuBtn.hide()
        self._ui.rightImage_graphicsView.view.setAspectLocked()
        self._ui.rightImage_graphicsView.view.invertX()

        self.roiRight = pg.LineSegmentROI([[10, 128],[492,128]],maxBounds=QRectF(0,0,512,512),pen='y')
        self._ui.rightImage_graphicsView.view.addItem(self.roiRight)
        self.roiRight.sigRegionChangeFinished.connect(self.updateRight)
        
  
    def pressSnapTop(self):
        
        self.connx.core.snapImage()      
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsTop = np.rot90(pixels)
        self.pixels_imageTop = pg.ImageItem(self.pixelsTop)
        self._ui.topImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.topImage_graphicsView.view.addItem(self.pixels_imageTop)

        print('T')

    def pressSnapBottom(self):
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsBottom = np.rot90(pixels)
        self.pixels_imageBottom = pg.ImageItem(self.pixelsBottom)
        self._ui.bottomImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.bottomImage_graphicsView.view.addItem(self.pixels_imageBottom)

        print('B')

    def pressSnapLeft(self):
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsLeft = np.rot90(pixels)
        self.pixels_imageLeft = pg.ImageItem(self.pixelsLeft)
        self._ui.leftImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.leftImage_graphicsView.view.addItem(self.pixels_imageLeft)

        print('L')

    def pressSnapRight(self):
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsRight = np.rot90(pixels)
        self.pixels_imageRight = pg.ImageItem(self.pixelsRight)
        self._ui.rightImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.rightImage_graphicsView.view.addItem(self.pixels_imageRight)

        print('R')

    def updateTop(self):
        self.boxDataTop = self.roiTop.getArraySlice(self.pixelsTop,self.pixels_imageTop,axes=(0,1))
        print('Top Box')
        print(self.boxDataTop)
        
    def updateBottom(self):
        self.boxDataBottom = self.roiBottom.getArraySlice(self.pixelsBottom,self.pixels_imageBottom,axes=(0,1))
        print('Bottom Box')
        print(self.boxDataBottom)

    def updateLeft(self):
        self.boxDataLeft = self.roiLeft.getArraySlice(self.pixelsLeft,self.pixels_imageLeft,axes=(0,1))
        print('Left Box')
        print(self.boxDataLeft)

    def updateRight(self):
        self.boxDataRight = self.roiRight.getArraySlice(self.pixelsRight,self.pixels_imageRight,axes=(0,1))
        print('Right Box')
        print(self.boxDataRight)
        
