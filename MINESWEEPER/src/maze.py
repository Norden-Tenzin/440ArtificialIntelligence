import random
import numpy as np
from constants import *

class Maze():
    def __init__(self):
        self.dim = DIM
        self.num_mine = NUM_MINES
        self.curr = self.emptyFieldMaker()
        self.answers = self.mineFieldMaker()

    def emptyFieldMaker(self):
        d = self.dim
        m = self.num_mine

        arr = [['?' for i in range(d)] for j in range(d)] 
        # print(np.array(arr))
        return arr

    """
    
    @arg bool original - 
    @return returns an array of the minefield. if original is True returns the hidden version.
    Otherwise returns the visible version.
    """
    def mineFieldMaker(self):
        d = self.dim
        m = self.num_mine

        arr = [['0' for i in range(d)] for j in range(d)] 
        while m != 0:
            row = random.randint(0, d-1)
            col = random.randint(0, d-1)
            curr = arr[row][col]
            if curr == "0" and m != 0:
                arr[row][col] = 'm'
                m -= 1

        for row, line in enumerate(arr):
            for col, item in enumerate(line):
                if arr[row][col] != "m":
                    mineNeighbors = self.findNeighboringMines((row, col), arr)
                    arr[row][col] = str(mineNeighbors)
        return arr

    def findNeighboringMines(self, pos, arr):
        x = pos[0]
        y = pos[1]
        mines = 0

        potential_neighbor = [(x, y - 1), (x -1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]

        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
                if arr[i][j] ==  "m":
                    mines += 1
        return mines