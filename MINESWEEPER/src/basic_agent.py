import numpy as np
import random
from constants import *

class basic_agent():
    global found
    global Boom
    global num_random_pick
    found = 0
    Boom = 0
    num_random_pick = 0
    
    def __init__(self, env):
        self.original_arr = env.getAnswers()
        self.copy_arr = env.getCurr()
        self.env = env
        self.hiddenNeighborCount = 0
        

    def run(self):
        global found
        global Boom
        global num_random_pick
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
                    if self.copy_arr[row][col] == '?' or self.copy_arr[row][col] == 'm' or self.copy_arr[row][col] == 'f':
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
                        print("random pick")
                        num_random_pick += 1
                        self.query((x, y))
                        break
                    
    def runStep(self):
        global found
        global Boom
        global num_random_pick
        
        hidden_neighb_num = 0
        if self.chech_unclicked():
            change = False
            # chech each cell
            print("TURN")
            for row, line in enumerate(self.env.getCurr()):
                for col, item in enumerate(line):
                    if item != "?" and item != "m" and item != "f":
                        self.hiddenNeighborCount = self.check_hidden_neighb(row, col, '?')
                        clue = int(self.env.getCurr()[row][col])
                        mine_neighb_num = self.check_hidden_neighb(row, col, 'm')
                        if self.hiddenNeighborCount != 0:
                            potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
                            if clue - mine_neighb_num == self.hiddenNeighborCount:
                                # all the hidden neighb are mine.
                                for (i, j) in potential_neighbor:
                                    if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                                        if self.env.getCurr()[i][j] ==  '?':
                                            self.env.getHelp()[i][j] = 'm'
                                            found += 1
                                            
                            if (8 - clue) -  (8 - mine_neighb_num - self.hiddenNeighborCount) == self.hiddenNeighborCount:
                                # all the hidden neighb are safe.
                                for (i, j) in potential_neighbor:
                                    if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                                        if self.env.getCurr()[i][j] ==  '?' and self.env.getHelp()[i][j] != "m":
                                            self.env.getHelp()[i][j] = 's'
  
    def chech_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False
    
    def query_all(self, row, col, status):
        global found
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                if self.copy_arr[i][j] ==  '?':
                    if status == "mine":
                        self.copy_arr[i][j] = 'f'
                        # print(np.array(self.copy_arr))
                        found += 1
                    if status == "safe":
                        self.copy_arr[i][j] = self.original_arr[i][j]
                        # print(np.array(self.copy_arr))

    def check_hidden_neighb(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        result = 0

        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                if status == 'm':
                    if self.env.getCurr()[i][j] ==  status or self.env.getCurr()[i][j] ==  'f':
                        result += 1
                else:
                    if self.env.getCurr()[i][j] ==  status:
                        result += 1
        return result
    
    def query(self, pos):
        global Boom
        x = pos[0]
        y = pos[1]
        # print(self.original_arr[x][y])
        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
            print(np.array(self.copy_arr))
        else:
            print("Boom!!")
            Boom += 1
            self.copy_arr[x][y] = self.original_arr[x][y]
            print(np.array(self.copy_arr))