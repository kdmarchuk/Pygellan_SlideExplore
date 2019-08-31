# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:55:32 2019

@author: Kyle
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as text


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

ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.annotate('Well 1', xy=(0,0),fontsize = 8, color='b',xytext=(1650,715),textcoords='data')
ax.annotate('Well 2', xy=(0,0),fontsize = 8, color='b',xytext=(2850,715),textcoords='data')
ax.annotate('Well 3', xy=(0,0),fontsize = 8, color='b',xytext=(4100,715),textcoords='data')
ax.annotate('Well 4', xy=(0,0),fontsize = 8, color='b',xytext=(5350,715),textcoords='data')
ax.annotate('Well 5', xy=(0,0),fontsize = 8, color='b',xytext=(1650,1915),textcoords='data')
ax.annotate('Well 6', xy=(0,0),fontsize = 8, color='b',xytext=(2850,1915),textcoords='data')
ax.annotate('Well 7', xy=(0,0),fontsize = 8, color='b',xytext=(4100,1915),textcoords='data')
ax.annotate('Well 8', xy=(0,0),fontsize = 8, color='b',xytext=(5350,1915),textcoords='data')

topPositions = np.array([[1700,45],[2950,45],[4200,45],[5450,45],[1700,1165],[2950,1165],[4200,1165],[5450,1165]])
bottomPositions = np.array([[1700,985],[2950,985],[4200,985],[5450,985],[1700,2105],[2950,2105],[4200,2105],[5450,2105]])
leftPositions = np.array([[1168,515],[2418,515],[3668,515],[4918,515],[1168,1635],[2418,1635],[3668,1635],[4918,1635]])
rightPositions = np.array([[2232,515],[3482,515],[4732,515],[5982,515],[2232,1635],[3482,1635],[4732,1635],[5982,1635]])

rectRed = patches.Rectangle((topPositions[0][0],topPositions[0][1]),400,400,linewidth=1,edgecolor='r',facecolor='none')
rectBlue = patches.Rectangle((bottomPositions[0][0],bottomPositions[0][1]),400,400,linewidth=1,edgecolor='b',facecolor='none')
rectGreen = patches.Rectangle((leftPositions[0][0],leftPositions[0][1]),400,400,linewidth=1,edgecolor='g',facecolor='none')
rectYellow = patches.Rectangle((rightPositions[0][0],rightPositions[0][1]),400,400,linewidth=1,edgecolor='y',facecolor='none')

ax.add_patch(rectRed)
ax.add_patch(rectBlue)
ax.add_patch(rectGreen)
ax.add_patch(rectYellow)

plt.show()