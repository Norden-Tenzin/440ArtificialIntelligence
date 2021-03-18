from PIL import Image
from constants import *
import os
import math

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

mineImagePath = os.path.join(THIS_FOLDER, './assets/mine.png')
mineImageSavePath = os.path.join(THIS_FOLDER, './assets/smallmine.png')

flagImagePath = os.path.join(THIS_FOLDER, './assets/flag.png')
flagImageSavePath = os.path.join(THIS_FOLDER, './assets/smallflag.png')
# os.remove(savePath)

def imageInit():
    mineImage = Image.open(mineImagePath)
    mineNewImage = mineImage.resize((math.ceil(CELLSIZE*0.75),math.ceil(CELLSIZE*0.75)))
    mineNewImage.save(mineImageSavePath)
    
    flagImage = Image.open(flagImagePath)
    flagNewImage = flagImage.resize((math.ceil(CELLSIZE*0.75),math.ceil(CELLSIZE*0.75)))
    flagNewImage.save(flagImageSavePath)