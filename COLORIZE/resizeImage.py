import numpy as np
import os
from PIL import Image
from constants import *

imagePaths = [BEACH1PATH, BEACH2PATH, BEACH3PATH, BEACH4PATH, BEACH5PATH]
resizedbeachPaths = [RESIZEBEACH1PATH, RESIZEBEACH2PATH, RESIZEBEACH3PATH, RESIZEBEACH4PATH, RESIZEBEACH5PATH]

basewidth = 600

for i, path in enumerate(imagePaths):
    img = Image.open(path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(resizedbeachPaths[i])