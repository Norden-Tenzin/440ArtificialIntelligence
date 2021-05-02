## @Sangkyun Kim @Tenzin Norden
## PROJECT 1 440 
import math

DIM = 16
DENSITY = 0.1
NUM_MINES = math.ceil((DIM*DIM) * DENSITY)

SIZE = 802
# MAZE_SIZE = 50
UI_SPACE = 400
# DIM = 16
# NUM_MINES = 80

SIDES = 2
DIFF = 2
DIFF_TOTAL = DIFF * (DIM-1)
CELLSIZE = int((SIZE-(2*SIDES)-DIFF_TOTAL)/DIM)
# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTDARK = (156, 169, 189)
DARK = (125, 135, 150)
DARKER = (90, 98, 111)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255,99,71)
LIGHTORANGE = (255, 157, 143)
YELLOW  = (255,255,0)

# Numbers Colors
NUMBER1 = (1,0,254)
NUMBER2 = (1,127,1)
NUMBER3 = (254,0,0)
NUMBER4 = (1,0,128)
NUMBER5 = (129,1,2)
NUMBER6 = (0,128,129)
NUMBER7 = (0,0,0)
NUMBER8 = (128,128,128)

# File Locations 
GAMEFILE = "./save/game.txt"
CLEANFILE = "./save/clean.txt"
FIREFILE = "./save/fire.txt"

# Fire spread probability 
Q = 0.01
P = 0.3

