import random
import numpy as np
import math

from constants import *
from maze import *

"""
    What to return
    - curr array. as changed by environment.
    -
    -
    
    NOTE: 
    maybe env should have its own maze.
    
"""

class Environment():
    def __init__(self):
        self.maze = Maze()

    """

        @arg bool original -
    """
    
    def getAnswers(self):
        return self.maze.answers
    
    def getCurr(self):
        return self.maze.curr
    
    def query(self, pos):
        newPos = self.translate(pos)
        print(newPos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            # print(x, y)
            if self.maze.answers[x][y] != 'm':
                self.maze.curr[x][y] = self.maze.answers[x][y]
                return self.maze.curr
            else:
                self.maze.curr[x][y] = 'm'
                return self.maze.curr

    def queryAgent(self, pos):
        if self.maze.answers[pos[0]][pos[1]] != 'm':
            self.maze.curr[pos[0]][pos[1]] = self.maze.answers[pos[0]][pos[1]]
            return self.maze.curr
        else:
            print("Boom!!")
            
    def translate(self, pos):
        print("POSX: " + str(pos[0]))
        print(CELLSIZE)
        col = math.floor(pos[0]/(CELLSIZE+DIFF))
        row = math.floor(pos[1]/(CELLSIZE+DIFF))
        
        return (row, col)
    