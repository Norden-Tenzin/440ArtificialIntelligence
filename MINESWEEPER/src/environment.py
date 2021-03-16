import random
import numpy as np

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
        if (pos[0] > 5 and pos[0] < 803) and (pos[1] > 5 and pos[1] < 803):
            col = pos[0]//(CELLSIZE+DIFF_TOTAL)
            row = pos[1]//(CELLSIZE+DIFF_TOTAL)
            
            return (row, col)
    