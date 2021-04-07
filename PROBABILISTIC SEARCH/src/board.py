import random
import numpy as np

from constants import *

class Board():
    def __init__(self):
        self.dim = DIM
        self.board = self.boardMaker()
        self.target = self.targetMaker()

    def targetMaker(self):
        #row = random.randint(0, DIM - 1)
        #col = row = random.randint(0, DIM - 1)

        for row in range(DIM):
            for col in range(DIM):
                if self.board[row][col] == 1:
                    result = (row , col)
                    break

        result = (row, col)

        print("Target position")
        print(result)

        return result

    def boardMaker(self):
        arr = [['0' for i in range(DIM)] for j in range(DIM)]

        for row, line in enumerate(arr):
            for col, item in enumerate(line):
                p = np.random.rand()
                """
                flat = 1
                hilly = 2
                forested = 3
                cave = 4
                """
                if p <= 0.25:
                    arr[row][col] = 1
                elif p > 0.25 and p <= 0.5:
                    arr[row][col] = 2
                elif p > 0.5 and p <= 0.75:
                    arr[row][col] = 3
                elif p > 0.75 and p <= 1:
                    arr[row][col] = 4

        # print(np.array(arr))
        return arr