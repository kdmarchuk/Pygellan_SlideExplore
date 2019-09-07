
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as text
import pyqtgraph as pg

class createIBIDI():
    def __init__(self):

        phys_to_img_conversion = 100

        ### Slide Parameters ###
        slideHeight_mm =  25.50
        slideWidth_mm = 75.60
        wellWidth_mm = 10.65
        wellHeight_mm = 9.41
        wellCtoCVert_mm = 11.2
        wellCtoCHor_mm = 12.5
        nWells = 8
        nRows = 2
        nColumns = 4
        wellPositions_mm = np.array([[7.15,19.0],[7.15,31.5],[7.15,44.0],[7.15,56.5],[18.35,19.0],[18.35,31.5],[18.35,44.1],[18.35,56.5]])

        ### Image Conversion ###
        slideHeight_pix = slideHeight_mm * phys_to_img_conversion
        slideWidth_pix = slideWidth_mm * phys_to_img_conversion
        wellHeight_pix = wellHeight_mm * phys_to_img_conversion
        wellHeight_pix = int(wellHeight_pix)
        wellWidth_pix = wellWidth_mm * phys_to_img_conversion
        wellWidth_pix = int(wellWidth_pix)
        wellCtoCVert_pix = wellCtoCVert_mm * phys_to_img_conversion
        wellCtoCVert_pix = int(wellCtoCVert_pix)
        wellCtoCHor_pix = wellCtoCHor_mm * phys_to_img_conversion
        wellCtoCHor_pix = int(wellCtoCHor_pix)
        wellPositions_pix = wellPositions_mm * phys_to_img_conversion
        self.wellPositions_pix = wellPositions_pix.astype(int)

        # Dictionary to move values around
        self.slideDictPix = {
            "numWells" : nWells,
            "numRows" : nRows,
            "numColumns" : nColumns,
            "slideHeight" : slideHeight_pix,
            "slideWidth" : slideWidth_pix,
            "wellHeight" : wellHeight_pix,
            "wellWidth" : wellWidth_pix,
            "wellCtCVert" : wellCtoCVert_pix,
            "wellCtCHor" : wellCtoCHor_pix
        }

        #### Create Slide Image ###
        slideArray = np.zeros((np.int(np.round(slideHeight_pix)),np.int(np.round(slideWidth_pix))),dtype=int)
        # Add Wells to Array
        for pos in self.wellPositions_pix:
            slideArray[pos[0]-int(wellHeight_pix/2):pos[0]+int(wellHeight_pix/2),pos[1]-int(wellWidth_pix/2):pos[1]+int(wellWidth_pix/2)] = 1

        slideArray = np.rot90(slideArray)
        self.slideBase = pg.ImageItem(slideArray)

        self.well1text = pg.TextItem(text='1',color='k')
        self.well1text.setPos(1650,315)
        #self._ui.selectedSlide_graphicsView.view.addItem(well1text)
        self.well2text = pg.TextItem(text='2',color='k')
        self.well2text.setPos(2900,315)
        #self._ui.selectedSlide_graphicsView.view.addItem(well2text)
        self.well3text = pg.TextItem(text='3',color='k')
        self.well3text.setPos(4150,315)
        #self._ui.selectedSlide_graphicsView.view.addItem(well3text)
        self.well4text = pg.TextItem(text='4',color='k')
        self.well4text.setPos(5400,315)
        #self._ui.selectedSlide_graphicsView.view.addItem(well4text)
        self.well5text = pg.TextItem(text='5',color='k')
        self.well5text.setPos(1650,1515)
        #self._ui.selectedSlide_graphicsView.view.addItem(well5text)
        self.well6text = pg.TextItem(text='6',color='k')
        self.well6text.setPos(2900,1515)
        #self._ui.selectedSlide_graphicsView.view.addItem(well6text)
        self.well7text = pg.TextItem(text='7',color='k')
        self.well7text.setPos(4150,1515)
        #self._ui.selectedSlide_graphicsView.view.addItem(well7text)
        self.well8text = pg.TextItem(text='8',color='k')
        self.well8text.setPos(5400,1515)
        #self._ui.selectedSlide_graphicsView.view.addItem(well8text)

        self.topPositions = np.array([[1700,45],[2950,45],[4200,45],[5450,45],[1700,1165],[2950,1165],[4200,1165],[5450,1165]])
        self.bottomPositions = np.array([[1700,985],[2950,985],[4200,985],[5450,985],[1700,2105],[2950,2105],[4200,2105],[5450,2105]])
        self.leftPositions = np.array([[1168,515],[2418,515],[3668,515],[4918,515],[1168,1635],[2418,1635],[3668,1635],[4918,1635]])
        self.rightPositions = np.array([[2232,515],[3482,515],[4732,515],[5982,515],[2232,1635],[3482,1635],[4732,1635],[5982,1635]])

        print('IBIDI 8 Well Slide Loaded')
        