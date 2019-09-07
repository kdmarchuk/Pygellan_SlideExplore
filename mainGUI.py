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
from SlideROIs import ROIsMap

import createBridge
import IBIDI_Slide


class MainView(QMainWindow):
    def __init__(self):
        
        super().__init__() 
        
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.connx = createBridge.Connection()
    
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

        self.roiTop = pg.LineSegmentROI([[10, 256],[492,256]],pen='r')
        self._ui.topImage_graphicsView.view.addItem(self.roiTop)
        self.roiTop.sigRegionChangeFinished.connect(self.updateTop)
        # Bottom Image
        self._ui.bottomImage_graphicsView.ui.histogram.hide()
        self._ui.bottomImage_graphicsView.ui.roiBtn.hide()
        self._ui.bottomImage_graphicsView.ui.menuBtn.hide()
        self._ui.bottomImage_graphicsView.view.setAspectLocked()
        self._ui.bottomImage_graphicsView.view.invertX()

        self.roiBottom = pg.LineSegmentROI([[10, 256],[492,256]],pen='b')
        self._ui.bottomImage_graphicsView.view.addItem(self.roiBottom)
        self.roiBottom.sigRegionChangeFinished.connect(self.updateBottom)
        # Left Image
        self._ui.leftImage_graphicsView.ui.histogram.hide()
        self._ui.leftImage_graphicsView.ui.roiBtn.hide()
        self._ui.leftImage_graphicsView.ui.menuBtn.hide()
        self._ui.leftImage_graphicsView.view.setAspectLocked()
        self._ui.leftImage_graphicsView.view.invertX()

        self.roiLeft = pg.LineSegmentROI([[256, 10],[256,492]],pen='g')
        self._ui.leftImage_graphicsView.view.addItem(self.roiLeft)
        self.roiLeft.sigRegionChangeFinished.connect(self.updateLeft)
        # right Image
        self._ui.rightImage_graphicsView.ui.histogram.hide()
        self._ui.rightImage_graphicsView.ui.roiBtn.hide()
        self._ui.rightImage_graphicsView.ui.menuBtn.hide()
        self._ui.rightImage_graphicsView.view.setAspectLocked()
        self._ui.rightImage_graphicsView.view.invertX()

        self.roiRight = pg.LineSegmentROI([[256,10],[256, 492]],pen='y')
        self._ui.rightImage_graphicsView.view.addItem(self.roiRight)
        self.roiRight.sigRegionChangeFinished.connect(self.updateRight)

        # Push Calculate Button
        self._ui.runCalc_pushButton.clicked.connect(self.pressRunCalc)

        # Push Slide ROIs Button
        self._ui.ROIMap_pushButton.clicked.connect(self.pressCreateROImap)
  
    def loadIBIDISlide(self):
        ## Load IBIDI 8 well slide
        self.slide = IBIDI_Slide.createIBIDI()
        # Pull the array from the class
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.slideBase)
        # Add text to visual wells 
        ## TODO: (turn into a for loop for generalization)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well1text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well2text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well3text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well4text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well5text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well6text) 
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well7text)
        self._ui.selectedSlide_graphicsView.view.addItem(self.slide.well8text)

        # Get center of well position for ROI calcs
        self.wellCenters = self.slide.wellPositions_pix
        print(self.wellCenters)

    def pressSnapTop(self):
        # To remove previous graphics rectangle
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.topRect)
        except AttributeError:
            pass

        topWell = self._ui.topWell_spinBox.value()
        # To not crash if no slide is selected
        try:
            self.topRect = QGraphicsRectItem(self.slide.topPositions[topWell-1][0],self.slide.topPositions[topWell-1][1], 400,400) 
        except AttributeError:
            print("Select a slide first")
            return
        self.topRect.setBrush(QColor("red"))

        # Get xyz positions on Snap
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
        # To remove previous graphics rectangle
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.bottomRect)
        except AttributeError:
            pass

        bottomWell = self._ui.bottomWell_spinBox.value()

        # To not crash if no slide is selected
        try:
            self.bottomRect = QGraphicsRectItem(self.slide.bottomPositions[bottomWell-1][0],self.slide.bottomPositions[bottomWell-1][1], 400,400) 
        except AttributeError:
            print("Select a slide first")
            return
        self.bottomRect.setBrush(QColor("blue"))
        
        # Get xyz positions on Snap
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
        # To remove previous graphics rectangle
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.leftRect)
        except AttributeError:
            pass

        leftWell = self._ui.leftWell_spinBox.value()

        # To not crash if no slide is selected
        try:
            self.leftRect = QGraphicsRectItem(self.slide.leftPositions[leftWell-1][0],self.slide.leftPositions[leftWell-1][1], 400,400) 
        except AttributeError:
            print("Select a slide first")
            return
        self.leftRect.setBrush(QColor("green"))

        # Get xyz positions on Snap
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
        # To remove previous graphics rectangle
        try:
            self._ui.selectedSlide_graphicsView.removeItem(self.rightRect)
        except AttributeError:
            pass

        rightWell = self._ui.rightWell_spinBox.value()

        # To not crash if no slide is selected
        try:
            self.rightRect = QGraphicsRectItem(self.slide.rightPositions[rightWell-1][0],self.slide.rightPositions[rightWell-1][1], 400,400)
        except AttributeError:
            print("Select a slide first")
            return

        self.rightRect.setBrush(QColor("yellow"))

        # Get xyz positions on Snap
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
        #print('Top Box')
        #print(self.boxDataTop)
     
    def updateBottom(self):
        self.boxDataBottom = self.roiBottom.getArraySlice(self.pixelsBottom,self.pixels_imageBottom,axes=(0,1))
        #print('Bottom Box')
        #print(self.boxDataBottom)

    def updateLeft(self):
        self.boxDataLeft = self.roiLeft.getArraySlice(self.pixelsLeft,self.pixels_imageLeft,axes=(0,1))
        #print('Left Box')
        #print(self.boxDataLeft)

    def updateRight(self):
        self.boxDataRight = self.roiRight.getArraySlice(self.pixelsRight,self.pixels_imageRight,axes=(0,1))
        #print('Right Box')
        #print(self.boxDataRight)

    def pressRunCalc(self):
        self.pixelSize = self.connx.core.getPixelSizeUm()

        boxDataTop = self.roiTop.getArraySlice(self.pixelsTop,self.pixels_imageTop,axes=(0,1))
        print('Top Box')
        sliceTopX = boxDataTop[0][0]
        sliceTopY = boxDataTop[0][1]
        self.sliceTopXstart = sliceTopX.start
        self.sliceTopXstop = sliceTopX.stop
        self.sliceTopYstart = sliceTopY.start
        self.sliceTopYstop = sliceTopY.stop

        boxDataBottom = self.roiBottom.getArraySlice(self.pixelsBottom,self.pixels_imageBottom,axes=(0,1))
        print('Bottom Box')
        sliceBottomX = boxDataBottom[0][0]
        sliceBottomY = boxDataBottom[0][1]
        self.sliceBottomXstart = sliceBottomX.start
        self.sliceBottomXstop = sliceBottomX.stop
        self.sliceBottomYstart = sliceBottomY.start
        self.sliceBottomYstop = sliceBottomY.stop
        

        self.boxDataLeft = self.roiLeft.getArraySlice(self.pixelsLeft,self.pixels_imageLeft,axes=(0,1))
        print('Left Box')
        print(self.boxDataLeft)

        self.boxDataRight = self.roiRight.getArraySlice(self.pixelsRight,self.pixels_imageRight,axes=(0,1))
        print('Right Box')
        print(self.boxDataRight)
        
        ## Tip
        tipDistance = self.xPositionLeft - self.xPositionRight
        tipHeight = self.zPositionLeft - self.zPositionRight
        tipRad = np.arctan(tipHeight/tipDistance)
        tipDeg = np.degrees(tipRad)
        tipDeg = round(tipDeg,2)
        tipDegString = str(tipDeg) + u"\u00B0 Tip"
        # If tiltHeight is negative, tilt is positive and vice versa

        ## Tilt
        tiltDistance = self.yPositionTop - self.yPositionBottom
        tiltHeight = self.zPositionTop - self.zPositionBottom
        tiltRad = np.arctan(tiltHeight/tiltDistance)
        tiltDeg = np.degrees(tiltRad)
        tiltDeg = round(tiltDeg,2)
        tiltDegString = str(tiltDeg) + u"\u00B0 Tilt"

        ## Rotation
        rotDistance = (self.sliceTopXstart - self.sliceTopXstop) * self.pixelSize
        rotHeight = (self.sliceTopYstart - self.sliceTopYstop) * self.pixelSize
        rotRad = np.arctan(rotHeight/rotDistance)
        rotDeg = np.degrees(rotRad)
        rotDeg = round(rotDeg,2)
        rotDegString = str(rotDeg) + u"\u00B0 Rot"

        # Updates the display strings on the GUI
        self._ui.calcRot_label.setText(_translate("MainWindow", rotDegString))
        self._ui.calcTilt_label.setText(_translate("MainWindow",tiltDegString))
        self._ui.calcTip_label_3.setText(_translate("MainWindow",tipDegString))

        self.calcSlideTop()
        self.calcSlideBottom()


    def calcSlideTop(self):
        self.stagePosTop = self.yPositionTop + (self.sliceTopYstart * self.pixelSize)
        print('Measured Top Pos')
        print(self.stagePosTop)

    def calcSlideBottom(self):
        self.stagePosBottom = self.yPositionBottom + (self.sliceBottomYstart * self.pixelSize)
        print('Measured Bottom Pos')
        print(self.stagePosBottom)

        slideH = self.slide.slideDictPix.get("slideHeight")
        wellCtCVert = self.slide.slideDictPix.get("wellCtCVert")
        nRows = self.slide.slideDictPix.get("numRows")

        self.stagePosBottomCalc = self.stagePosTop + ((((nRows - 1) * wellCtCVert) + slideH) * self.pixelSize)
        print(['Calc Bottom Pos'])
        print(self.stagePosBottomCalc)




    def pressCreateROImap(self):
        self._ROIs_map = ROIsMap(self.slide)
        self._ROIs_map.show()



        
