import numpy as np
import random
from constants import *

class basic_agent():

    def __init__(self, original_arr, copy_arr):
        self.original_arr = original_arr
        self.copy_arr = copy_arr

    def run(self):
        playing = True
        # print(np.array(self.copy_arr))
        self.query(0, 0)
        hidden_neighb_num = 0
        
        # while agent is alive or not done
        while not np.array_equal(self.original_arr, self.copy_arr):
            change = False

            # chech each cell
            for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    # '?' or flag
                    if self.copy_arr[row][col] == '?' or self.copy_arr[row][col] == 'm':
                        continue
                    # clue
                    else:
                        hidden_neighb_num = self.check_hidden_neighb(row, col, '?')
                        clue = int(self.copy_arr[row][col])
                        mine_neighb_num = self.check_hidden_neighb(row, col, 'm')
                        """
                        print("----------------------------------")
                        print(hidden_neighb_num)
                        print(clue)
                        print(mine_neighb_num)
                        print((8 - clue) -  (8 - mine_neighb_num - hidden_neighb_num))
                        print("----------------------------------")
                        """
                        if hidden_neighb_num != 0:
                            if clue - mine_neighb_num == hidden_neighb_num:
                                # all the hidden neighb are mine.
                                self.query_all(row, col, "mine")
                                print(np.array(self.copy_arr))
                                change = True
                            if (8 - clue) -  (8 - mine_neighb_num - hidden_neighb_num) == hidden_neighb_num:
                                # all the hidden neighb are safe.
                                self.query_all(row, col, "safe")
                                print(np.array(self.copy_arr))
                                change = True
            if not change:
                while True:
                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)

                    if self.copy_arr[x][y] == '?':
                        print("random pick")
                        self.query(x, y)
                        break

        print(np.array(self.copy_arr))           

    def query_all(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                if self.copy_arr[i][j] ==  '?':
                    if status == "mine":
                        self.copy_arr[i][j] = 'm'       
                    if status == "safe":
                        self.copy_arr[i][j] = self.original_arr[i][j]

    def check_hidden_neighb(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        result = 0

        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                if self.copy_arr[i][j] ==  status:
                    result += 1
        return result
    
    def query(self, x, y):
        print(self.original_arr[x][y])
        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
        else:
            print("Boom!!")
            exit()