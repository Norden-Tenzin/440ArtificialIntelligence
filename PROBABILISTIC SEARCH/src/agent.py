import numpy as np
import random

from constants import *

class Agent():
    def __init__(self, environment, agentType):
        # self.originalBoard = game.board
        self.env = environment
        self.belief = np.full((DIM, DIM), 1 / DIM**2)
        self.belief2 = np.full((DIM, DIM), 1 / DIM**2)
        # self.target = game.target
        self.searchNum = 1
        self.distNum = 0
        self.agentType = agentType

    def run(self):
        # random start point
        curr = (random.randint(0, DIM - 1), random.randint(0, DIM - 1))  
        while True:
            result = self.env.search(curr)
            if result[0]:
                return (self.searchNum, self.distNum) 
            currNegRate = result[1]
            # update curr cell
            # P(B | not A) = (P(not A | B) P(B)) / P(not A)
            probNotinCurrCell = ((self.belief[curr[0]][curr[1]] * currNegRate) + (1 - self.belief[curr[0]][curr[1]]))
            self.belief[curr[0]][curr[1]] *= currNegRate
            # update other cells
            self.belief = self.belief / probNotinCurrCell
            if self.agentType == "agent2":
                for row in range(DIM):
                    for col in range(DIM):
                        self.belief2[row][col] = self.belief[row][col] * (1 - self.env.getNegRate((row, col))) 
                self.belief2 = self.belief2 / np.sum(self.belief2)
            self.searchNum += 1
            curr = self.maxProbMinDist(curr)

    def maxProbMinDist(self, curr):
        maxProbMinDistList = []
        minDistVal = 100

        if self.agentType == "agent2":
            maxVal = np.max(self.belief2)
            beliefType = self.belief2
        else:
            maxVal = np.max(self.belief)
            beliefType = self.belief
        for row in range(DIM):
            for col in range(DIM):
                if beliefType[row][col] == maxVal:
                    if self.getDist(curr, (row, col)) < minDistVal:
                        maxProbMinDistList.clear()
                        maxProbMinDistList.append((row, col))
                        minDistVal = self.getDist(curr, (row, col))
                    elif self.getDist(curr, (row, col)) == minDistVal:
                        maxProbMinDistList.append((row, col))
        self.distNum += minDistVal
        if len(maxProbMinDistList) > 1:
            return random.choice(maxProbMinDistList)
        elif len(maxProbMinDistList) == 1:
            return maxProbMinDistList[0]

    def getDist(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    
