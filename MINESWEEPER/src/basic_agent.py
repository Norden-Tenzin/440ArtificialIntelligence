import numpy as np
import random
from constants import *

class basic_agent():
    
    def __init__(self, original_arr, copy_arr, f):
        self.original_arr = original_arr
        self.copy_arr = copy_arr
        self.result_file = f
        self.found = 0
        self.Boom = 0
        self.num_random_pick = 0

    def run(self):
        # print(np.array(self.copy_arr))
        self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))
        hidden_neighb_num = 0
        
        # while agent is alive or not done

        while self.chech_unclicked():
            change = False

            # chech each cell
            for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    # '?' or flag or missed mine
                    if self.copy_arr[row][col] == '?' or self.copy_arr[row][col] == 'm' or self.copy_arr[row][col] == 'F':
                        continue
                    # clue
                    else:
                        hidden_neighb_num = self.check_hidden_neighb(row, col, '?')
                        clue = int(self.copy_arr[row][col])
                        mine_neighb_num = self.check_hidden_neighb(row, col, 'm')
                        
                        if hidden_neighb_num != 0:
                            if clue - mine_neighb_num == hidden_neighb_num:
                                # all the hidden neighb are mine.
                                self.query_all(row, col, "mine")
                                # print(np.array(self.copy_arr))
                                change = True
                            if (8 - clue) -  (8 - mine_neighb_num - hidden_neighb_num) == hidden_neighb_num:
                                # all the hidden neighb are safe.
                                self.query_all(row, col, "safe")
                                # print(np.array(self.copy_arr))
                                change = True
            if not change:
                while self.chech_unclicked():
                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)

                    if self.copy_arr[x][y] == '?':
                        # print("random pick")
                        self.num_random_pick += 1
                        self.query((x, y))
                        break
        """
        print("Basic Agent")
        print('%d x %d'%(DIM, DIM))
        print('total number of mine: %d'%(NUM_MINES))
        print('found : %d'%(self.found))
        print('Boom : %d'%(self.Boom))
        print('number of random pick : %d'%(self.num_random_pick))
        print('game socre: %d'%(self.found * (100 / NUM_MINES)))
        # print(np.array(self.original_arr))
        # print(np.array(self.copy_arr))
        """
        self.result_file.write('%d\n'%(self.found * (100 / NUM_MINES)))
        return self.found * (100 / NUM_MINES)

    # check each cell whether there are unclicked cell (cell with '?')
    # This is for the ending condition
    def chech_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False
    
    def query_all(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                if self.copy_arr[i][j] ==  '?':
                    if status == "mine":
                        self.copy_arr[i][j] = 'F'
                        # print(np.array(self.copy_arr))
                        self.found += 1
                    if status == "safe":
                        self.copy_arr[i][j] = self.original_arr[i][j]
                        # print(np.array(self.copy_arr))

    def check_hidden_neighb(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        result = 0

        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                if status == 'm':
                    if self.copy_arr[i][j] ==  status or self.copy_arr[i][j] ==  'F':
                        result += 1
                else:
                    if self.copy_arr[i][j] ==  status:
                        result += 1
        return result
    
    def query(self, pos):
        x = pos[0]
        y = pos[1]
        # print(self.original_arr[x][y])
        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
            # print(np.array(self.copy_arr))
        else:
            # print("Boom!!")
            self.Boom += 1
            self.copy_arr[x][y] = self.original_arr[x][y]
            # print(np.array(self.copy_arr))