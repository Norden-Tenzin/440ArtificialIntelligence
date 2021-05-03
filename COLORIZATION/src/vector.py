import numpy as np
import matplotlib.pyplot as plt
import random as rd
import os
from PIL import Image
from constants import *
from helper import *

def colorToBw():
    currImg = plt.imread(RESIZE_BEACH1_PATH)
    flatImg = np.array(currImg.reshape(-1, 3))
    for pix in range(len(flatImg)):
        r, g, b = flatImg[pix]
        grey = .21 * r + .72 * g + .07 * b
        flatImg[pix] = grey
    return flatImg.reshape(currImg.shape)


'''
# Saves the greyscale image

newimg = Image.fromarray(greyMatrix, 'RGB')
newimg.save(GREY_IMAGE_PATH)
newimg.show()
'''

currImg = plt.imread(RESIZE_BEACH1_PATH)
flatImg = np.array(currImg.reshape(-1, 3))

'''
# 3d plot of the flatImg data

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(flatImg[:,0],flatImg[:,1],flatImg[:,2], s=1)
ax.set_xlabel('R')
ax.set_xlabel('G')
ax.set_xlabel('B')
plt.show()
'''

# greyMatrix = colorToBw()
# plt.imshow(currImg)
# plt.show()

kMeans()
