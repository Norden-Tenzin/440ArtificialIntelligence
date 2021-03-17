from PIL import Image
from constants import *
import os
import math

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
questionImagePath = os.path.join(THIS_FOLDER, './assets/question.png')
questionImageSavePath = os.path.join(THIS_FOLDER, './assets/smallquestion.png')

mineImagePath = os.path.join(THIS_FOLDER, './assets/mine.png')
mineImageSavePath = os.path.join(THIS_FOLDER, './assets/smallmine.png')

flagImagePath = os.path.join(THIS_FOLDER, './assets/flag.png')
flagImageSavePath = os.path.join(THIS_FOLDER, './assets/smallflag.png')
# os.remove(savePath)

def imageInit():
    questionImage = Image.open(questionImagePath)
    questionNewImage = questionImage.resize((math.ceil(CELLSIZE*0.75),math.ceil(CELLSIZE*0.75)))
    questionNewImage.save(questionImageSavePath)
    
    mineImage = Image.open(mineImagePath)
    mineNewImage = mineImage.resize((math.ceil(CELLSIZE*0.75),math.ceil(CELLSIZE*0.75)))
    mineNewImage.save(mineImageSavePath)
    
    flagImage = Image.open(flagImagePath)
    flagNewImage = flagImage.resize((math.ceil(CELLSIZE*0.75),math.ceil(CELLSIZE*0.75)))
    flagNewImage.save(flagImageSavePath)