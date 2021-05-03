import numpy as np
import os
from PIL import Image
from constants import *

imagePaths = [BEACH1_PATH, BEACH2_PATH, BEACH3_PATH, BEACH4_PATH, BEACH5_PATH]
resizedbeachPaths = [RESIZE_BEACH1_PATH, RESIZE_BEACH2_PATH, RESIZE_BEACH3_PATH, RESIZE_BEACH4_PATH, RESIZE_BEACH5_PATH]

basewidth = 600

for i, path in enumerate(imagePaths):
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(resizedbeachPaths[i])