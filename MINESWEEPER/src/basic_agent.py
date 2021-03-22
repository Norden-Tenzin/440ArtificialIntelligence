import numpy as np
import random
from constants import *

class basic_agent():
    def __init__(self, env):
        self.env = env

        # variables that are defaulted to 0
        self.randomPickCount = 0

    def run(self):
        self.env.queryAgent((random.randint(0, DIM-1), random.randint(0, DIM-1)))
        # while agent is alive or not done
        while self.checkIfUnClicked():
            change = False
            # chech each cell
            for row, line in enumerate(self.env.getCurr()):
                for col, item in enumerate(line):
                    # '?' or flag or missed mine
                    if item != "?" and item != "m" and item != "f":
                        hiddenNeighborCount = self.checkHiddenNeighbor(row, col, '?')
                        clue = int(self.env.getCurr()[row][col])
                        mine_neighb_num = self.checkHiddenNeighbor(row, col, 'm')
                        
                        if hiddenNeighborCount != 0:
                            if clue - mine_neighb_num == hiddenNeighborCount:
                                # all the hidden neighb are mine.
                                self.queryAll(row, col, "mine")
                                change = True
                            if (8 - clue) -  (8 - mine_neighb_num - hiddenNeighborCount) == hiddenNeighborCount:
                                # all the hidden neighb are safe.
                                self.queryAll(row, col, "safe")
                                change = True
            if not change:
                while self.checkIfUnClicked():
                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)
                    if self.env.getCurr()[x][y] == '?':
                        self.randomPickCount += 1
                        self.env.queryAgent((x, y))
                        break
       
        # print("Basic Agent")
        # print('%d x %d'%(DIM, DIM))
        # print('total number of mine: %d'%(NUM_MINES))
        # print('found : %d'%(self.env.found))
        # print('Boom : %d'%(self.env.boom))
        # print('number of random pick : %d'%(self.randomPickCount))
        # print('game socre: %d'%(self.env.found * (100 / NUM_MINES)))
        return (self.env.found * (100 / NUM_MINES))
      
    def runStep(self):
        if self.checkIfUnClicked():
            change = False
            # checks each cell 
            for row, line in enumerate(self.env.getCurr()):
                for col, item in enumerate(line):
                    if item != "?" and item != "m" and item != "f":
                        hiddenNeighborCount = self.checkHiddenNeighbor(row, col, '?')
                        clue = int(self.env.getCurr()[row][col])
                        mine_neighb_num = self.checkHiddenNeighbor(row, col, 'm')
                        if hiddenNeighborCount != 0:
                            potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
                            if clue - mine_neighb_num == hiddenNeighborCount:
                                # all the hidden neighb are mine.
                                for (i, j) in potential_neighbor:
                                    if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                                        if self.env.getCurr()[i][j] ==  '?':
                                            self.env.getHelp()[i][j] = 'm'                                            
                            if (8 - clue) -  (8 - mine_neighb_num - hiddenNeighborCount) == hiddenNeighborCount:
                                # all the hidden neighb are safe.
                                for (i, j) in potential_neighbor:
                                    if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                                        if self.env.getCurr()[i][j] ==  '?' and self.env.getHelp()[i][j] != "m":
                                            self.env.getHelp()[i][j] = 's'
    
    def checkIfUnClicked(self):
        for row, line in enumerate(self.env.getCurr()):
                for col, item in enumerate(line):
                    if item == '?':
                        return True
        return False
    def queryAll(self, row, col, status):
        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.env.getCurr())) and (j >= 0 and j < len(self.env.getCurr())):
                if self.env.getCurr()[i][j] ==  '?':
                    if status == "mine":
                        self.env.flagAgent((i, j))
                    if status == "safe":
                        self.env.queryAgent((i, j))

    def checkHiddenNeighbor(self, row, col, status):
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
