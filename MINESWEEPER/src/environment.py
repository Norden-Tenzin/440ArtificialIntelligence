import random
import numpy as np

class Environment():
    def __init__(self, dim, num_mine):
        self.dim = dim
        self.num_mine = num_mine
        self.hidden = self.mineFieldMaker(False)
        self.shown = self.mineFieldMaker(True)


    """
    
    @arg bool original - 
    """
    def mineFieldMaker(self, original):
        finalPath = []
        d = self.dim
        m = self.num_mine

        arr = [['0' for i in range(d)] for j in range(d)] 

        if not original:
            for row, line in enumerate(arr):
                for col, item in enumerate(line):
                    arr[row][col] = "?"
            return arr

        for i in range(m):
            row = random.randint(0, d-1)
            col = random.randint(0, d-1)
            curr = arr[row][col]
            if curr == "0" and m != 0:
                arr[row][col] = 'm'
                m -= 1

        for row, line in enumerate(arr):
            for col, item in enumerate(line):
                if arr[row][col] != "m":
                    mineNeighbors = findMines((row, col), arr)
                    arr[row][col] = str(mineNeighbors)
        return arr

def findMines(pos, arr):
    x = pos[0]
    y = pos[1]
    mines = 0

    potential_neighbor = [(x, y - 1), (x -1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]

    for (i, j) in potential_neighbor:
        if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
            if arr[i][j] ==  "m":
                mines += 1
    return mines