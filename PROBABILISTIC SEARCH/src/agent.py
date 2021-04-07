import numpy as np
import random

from constants import *

class Agent():
    def __init__(self, game, agentType):
        self.originalBoard = game.board
        self.belief = np.full((DIM, DIM), 1 / DIM**2)
        self.belief2 = np.full((DIM, DIM), 1 / DIM**2)
        self.target = game.target
        self.searchNum = 1
        self.distNum = 0
        self.agentType = agentType

    def run(self):
        
        # random start point
        curr = (random.randint(0, DIM - 1), random.randint(0, DIM - 1))
        print("Initial position")
        print(curr)
        print("Target in")
        print(self.originalBoard[self.target[0]][self.target[1]])
        currNegRate = self.getNegRate(curr)
        # print(currNegRate)
        
        while True:
            
            if curr == self.target:
                p = random.uniform(0, 1)
                currNegRate = self.getNegRate(curr)
                if p > currNegRate:
                    return (self.searchNum, self.distNum) 
            
            # update curr cell
            # P(B | not A) = (P(not A | B) P(B)) / P(not A)
            probNotinCurrCell = ((self.belief[curr[0]][curr[1]] * currNegRate) + (1 - self.belief[curr[0]][curr[1]]))
            self.belief[curr[0]][curr[1]] *= currNegRate
            # print(self.belief[curr[0]][curr[1]])
            # update other cells
            self.belief = self.belief / probNotinCurrCell
            
            if self.agentType == "agent2":
                for row in range(DIM):
                    for col in range(DIM):
                        self.belief2[row][col] = self.belief[row][col] * (1 - self.getNegRate((row, col))) 
                self.belief2 = self.belief2 / np.sum(self.belief2)

            #print(np.array(self.belief))
            self.searchNum += 1

            # select cell with highest prob
            # if there are several cells with the highest prob -> select cell with shortest dist from curr
            # if there are same high prob and same dist -> select random
            curr = self.maxProbMinDist(curr)
            #print("selected position")
            #print(curr)
            #print("--------------------------------------")

            

    def maxProbMinDist(self, curr):
        maxProbMinDistList = []
        minDistVal = 100

        if self.agentType == "agent2":
            maxVal = np.max(self.belief2)
            beliefType = self.belief2
        else:
            maxVal = np.max(self.belief)
            beliefType = self.belief
        #print(maxVal)

        for row in range(DIM):
            for col in range(DIM):
                if beliefType[row][col] == maxVal:
                    if self.getDist(curr, (row, col)) < minDistVal:
                        maxProbMinDistList.clear()
                        maxProbMinDistList.append((row, col))
                        minDistVal = self.getDist(curr, (row, col))
                    elif self.getDist(curr, (row, col)) == minDistVal:
                        maxProbMinDistList.append((row, col))
                        # minDistVal = self.getDist(curr, (row, col))

        # print(maxProbMinDistList)
        self.distNum += minDistVal

        if len(maxProbMinDistList) > 1:
            return random.choice(maxProbMinDistList)
        elif len(maxProbMinDistList) == 1:
            return maxProbMinDistList[0]

    def getDist(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        

    def getNegRate(self, pos):
        row = pos[0]
        col = pos[1]

        if self.originalBoard[row][col] == 1:
            return 0.1
        elif self.originalBoard[row][col] == 2:
            return 0.3
        elif self.originalBoard[row][col] == 3:
            return 0.7
        elif self.originalBoard[row][col] == 4:
            return 0.9
