from environment import *
from maze import *
from cell import *
from itertools import *

from constants import *
from knowledge import *
import numpy as np
import math
# en = Maze(DIM, NUM_MINES)
# print(np.array(en.shown))
# print(np.array(en.hidden))

# cell = Cell("s")
# print(cell.state)

# know = Knowledge()
# print(np.array(know.arr))

def main():
    arr = [[(0, 7), (1, 8), (1, 7)], [(0, 0), (1, 1)]]
    print(list(product(*arr)))

if __name__ == "__main__":
    main()