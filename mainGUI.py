# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:05:34 2019

@author: Kyle

Main window of the GUI. 
"""

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QAbstractItemView, QMessageBox, QGraphicsRectItem
from PyQt5.QtCore import pyqtSlot, Qt, QRectF, QCoreApplication
from PyQt5.QtGui import QPixmap, QColor
_translate = QCoreApplication.translate

import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg

from mainGUI_ui import Ui_MainWindow

import createBridge
#import IBIDI_Slide


class MainView(QMainWindow):
    def __init__(self):
        
        super().__init__() 
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.connx = createBridge.Connection()
        #self.channelGroup = self.connx.core.getChannelGroup()
        #print(self.channelGroup)
    
        ### Connections for Days
        # Select Slide Dropdown
        self._ui.actionIbidi_8_Well.triggered.connect(self.loadIBIDISlide)

        self._ui.selectedSlide_graphicsView.ui.menuBtn.hide()
        self._ui.selectedSlide_graphicsView.ui.histogram.hide()
        self._ui.selectedSlide_graphicsView.ui.roiBtn.hide()
        self._ui.selectedSlide_graphicsView.view.setAspectLocked()

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

        # Push Calculate Button
        self._ui.runCalc_pushButton.clicked.connect(self.pressRunCalc)
  
    def loadIBIDISlide(self):
        #IBIDI_Slide.createIBIDI()
        phys_to_img_conversion = 100

        ### Slide Parameters ###
        slideHeight_mm =  25.50
        slideWidth_mm = 75.60
        wellWidth_mm = 10.65
        wellHeight_mm = 9.41
        nWells = 8
        wellPositions_mm = np.array([[7.15,19.0],[7.15,31.5],[7.15,44.0],[7.15,56.5],[18.35,19.0],[18.35,31.5],[18.35,44.1],[18.35,56.5]])

        ### Image Conversion ###
        slideHeight_pix = slideHeight_mm * phys_to_img_conversion
        slideWidth_pix = slideWidth_mm * phys_to_img_conversion
        wellHeight_pix = wellHeight_mm * phys_to_img_conversion
        wellHeight_pix = int(wellHeight_pix)
        wellWidth_pix = wellWidth_mm * phys_to_img_conversion
        wellWidth_pix = int(wellWidth_pix)
        wellPositions_pix = wellPositions_mm * phys_to_img_conversion
        wellPositions_pix = wellPositions_pix.astype(int)

        #### Create Slide Image ###
        slideArray = np.zeros((np.int(np.round(slideHeight_pix)),np.int(np.round(slideWidth_pix))),dtype=int)
        # Add Wells to Array
        for pos in wellPositions_pix:
            slideArray[pos[0]-int(wellHeight_pix/2):pos[0]+int(wellHeight_pix/2),pos[1]-int(wellWidth_pix/2):pos[1]+int(wellWidth_pix/2)] = 1
        
        #plt.figure(1)
        #plt.imshow(slideArray,cmap='gray')
        #plt.show()
        slideArray = np.rot90(slideArray)
        slideBase = pg.ImageItem(slideArray)
        self._ui.selectedSlide_graphicsView.view.addItem(slideBase)
        well1text = pg.TextItem(text='1',color='k')
        well1text.setPos(1650,315)
        self._ui.selectedSlide_graphicsView.view.addItem(well1text)
        well2text = pg.TextItem(text='2',color='k')
        well2text.setPos(2900,315)
        self._ui.selectedSlide_graphicsView.view.addItem(well2text)
        well3text = pg.TextItem(text='3',color='k')
        well3text.setPos(4150,315)
        self._ui.selectedSlide_graphicsView.view.addItem(well3text)
        well4text = pg.TextItem(text='4',color='k')
        well4text.setPos(5400,315)
        self._ui.selectedSlide_graphicsView.view.addItem(well4text)
        well5text = pg.TextItem(text='5',color='k')
        well5text.setPos(1650,1515)
        self._ui.selectedSlide_graphicsView.view.addItem(well5text)
        well6text = pg.TextItem(text='6',color='k')
        well6text.setPos(2900,1515)
        self._ui.selectedSlide_graphicsView.view.addItem(well6text)
        well7text = pg.TextItem(text='7',color='k')
        well7text.setPos(4150,1515)
        self._ui.selectedSlide_graphicsView.view.addItem(well7text)
        well8text = pg.TextItem(text='8',color='k')
        well8text.setPos(5400,1515)
        self._ui.selectedSlide_graphicsView.view.addItem(well8text)

    def pressSnapTop(self):
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.topRect)
        except AttributeError:
            self.topRect = "Initialized Value"

        topWell = self._ui.topWell_spinBox.value()
        topPositions = np.array([[1700,45],[2950,45],[4200,45],[5450,45],[1700,1165],[2950,1165],[4200,1165],[5450,1165]]) 
        self.topRect = QGraphicsRectItem(topPositions[topWell-1][0],topPositions[topWell-1][1], 400,400) 
        self.topRect.setBrush(QColor("red"))

        self.zPositionTop = self.connx.core.getPosition()
        self.xPositionTop = self.connx.core.getXPosition()
        self.yPositionTop = self.connx.core.getYPosition()  
        self.connx.core.snapImage()      
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsTop = np.rot90(pixels)
        self.pixels_imageTop = pg.ImageItem(self.pixelsTop)
        self._ui.topImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.topImage_graphicsView.view.addItem(self.pixels_imageTop)
        self._ui.selectedSlide_graphicsView.view.addItem(self.topRect)
        
        print('T')

    def pressSnapBottom(self):
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.bottomRect)
        except AttributeError:
            self.bottomRect = "Initialized Value"
        bottomWell = self._ui.bottomWell_spinBox.value()
        bottomPositions = np.array([[1700,985],[2950,985],[4200,985],[5450,985],[1700,2105],[2950,2105],[4200,2105],[5450,2105]])
        self.bottomRect = QGraphicsRectItem(bottomPositions[bottomWell-1][0],bottomPositions[bottomWell-1][1], 400,400) 
        self.bottomRect.setBrush(QColor("blue"))

        self.zPositionBottom = self.connx.core.getPosition() 
        self.xPositionBottom = self.connx.core.getXPosition()
        self.yPositionBottom = self.connx.core.getYPosition() 
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsBottom = np.rot90(pixels)
        self.pixels_imageBottom = pg.ImageItem(self.pixelsBottom)
        self._ui.bottomImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.bottomImage_graphicsView.view.addItem(self.pixels_imageBottom)
        self._ui.selectedSlide_graphicsView.view.addItem(self.bottomRect)

        print('B')

    def pressSnapLeft(self):
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.leftRect)
        except AttributeError:
            self.leftRect = "Initialized Value"
        leftWell = self._ui.leftWell_spinBox.value()
        leftPositions = np.array([[1168,515],[2418,515],[3668,515],[4918,515],[1168,1635],[2418,1635],[3668,1635],[4918,1635]])
        self.leftRect = QGraphicsRectItem(leftPositions[leftWell-1][0],leftPositions[leftWell-1][1], 400,400) 
        self.leftRect.setBrush(QColor("green"))

        self.zPositionLeft = self.connx.core.getPosition()
        self.xPositionLeft = self.connx.core.getXPosition()
        self.yPositionLeft = self.connx.core.getYPosition()  
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsLeft = np.rot90(pixels)
        self.pixels_imageLeft = pg.ImageItem(self.pixelsLeft)
        self._ui.leftImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.leftImage_graphicsView.view.addItem(self.pixels_imageLeft)
        self._ui.selectedSlide_graphicsView.view.addItem(self.leftRect)

        print('L')

    def pressSnapRight(self):
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.rightRect)
        except AttributeError:
            self.rightRect = "Initialized Value"
        rightWell = self._ui.rightWell_spinBox.value()
        rightPositions = np.array([[2232,515],[3482,515],[4732,515],[5982,515],[2232,1635],[3482,1635],[4732,1635],[5982,1635]])
        self.rightRect = QGraphicsRectItem(rightPositions[rightWell-1][0],rightPositions[rightWell-1][1], 400,400) 
        self.rightRect.setBrush(QColor("yellow"))

        self.zPositionRight = self.connx.core.getPosition()
        self.xPositionRight = self.connx.core.getXPosition()
        self.yPositionRight = self.connx.core.getYPosition()  
        self.connx.core.snapImage()
        tagged_image = self.connx.core.getTaggedImage()
        pixels_flat = tagged_image[0]
        metadata = tagged_image[1]
        pixels = np.reshape(pixels_flat,newshape=[metadata['Height'],metadata['Width']])
        self.pixelsRight = np.rot90(pixels)
        self.pixels_imageRight = pg.ImageItem(self.pixelsRight)
        self._ui.rightImage_graphicsView.view.setMouseEnabled(x=False,y=False)
        self._ui.rightImage_graphicsView.view.addItem(self.pixels_imageRight)
        self._ui.selectedSlide_graphicsView.view.addItem(self.rightRect)

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

    def pressRunCalc(self):

        ## Change to Tip!!!
        tiltDistance = self.xPositionLeft - self.xPositionRight
        print(tiltDistance)
        tiltHeight = self.zPositionLeft - self.zPositionRight
        print(tiltHeight)
        tiltRad = np.arctan(tiltHeight/tiltDistance)
        print(tiltRad)
        tiltDeg = np.degrees(tiltRad)
        print(tiltDeg)

        # If tiltHeight is negative, tilt is positive and vice versa


        self._ui.calcRot_label.setText(_translate("MainWindow", "42 Degrees"))
        self._ui.calcTilt_label.setText(_translate("MainWindow","0.2 Degrees"))
        self._ui.calcTip_label_3.setText(_translate("MainWindow","90 Degrees"))

        
