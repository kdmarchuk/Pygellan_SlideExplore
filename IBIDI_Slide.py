
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as text
import pyqtgraph as pg

from mainGUI import MainView

class createIBIDI():
    def __init__(self):
        #self._ui = Ui_MainWindow()
        
        print('Hello!')

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
        
        plt.figure(1)
        plt.imshow(slideArray,cmap='gray')

        plt.show()

        slideBase = pg.ImageItem(slideArray)

        self._ui.selectedSlide_graphicsView.view.addItem(slideBase)
        