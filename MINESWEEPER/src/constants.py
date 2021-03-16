## @Sangkyun Kim @Tenzin Norden
## PROJECT 1 440 

SIZE = 808
# MAZE_SIZE = 50
UI_SPACE = 400
DIM = 5
NUM_MINES = 5

SIDES = 5
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
ORANGE = (255, 69, 0)
LIGHTORANGE = (255, 157, 143)
YELLOW  = (255,255,0)

# File Locations 
GAMEFILE = "./save/game.txt"
CLEANFILE = "./save/clean.txt"
FIREFILE = "./save/fire.txt"

# Fire spread probability 
Q = 0.01
P = 0.3

