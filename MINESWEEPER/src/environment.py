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
    def newMaze(self):
        self.maze = Maze()
    
    def resetMaze(self):
        self.maze.resetMaze()
    
    def getAnswers(self):
        return self.maze.answers
    
    def getCurr(self):
        return self.maze.curr
    
    # def choices(self, arr):
    #     print("\n")
    #     print(np.array(arr))
        
    
    # def findNeighboringMines(self, pos, arr):
    #     x = pos[0]
    #     y = pos[1]
    #     mines = 0
    #     choices = []
        
    #     potential_neighbor = [(x, y - 1), (x -1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]

    #     for (i, j) in potential_neighbor:
    #         if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
    #             if arr[i][j] ==  "?":
    #                 choices.append((i, j))
    #     return choices
    
    def query(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.maze.answers[x][y] != 'm':
                self.maze.curr[x][y] = self.maze.answers[x][y]
                # self.choices(self.maze.curr)
                return self.maze.curr
            else:
                self.maze.curr[x][y] = 'm'
                # self.choices(self.maze.curr)
                return self.maze.curr

    def queryAgent(self, pos):
        if self.maze.answers[pos[0]][pos[1]] != 'm':
            self.maze.curr[pos[0]][pos[1]] = self.maze.answers[pos[0]][pos[1]]
            return self.maze.curr
        else:
            print("Boom!!")
            
    def flag(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.maze.curr[x][y] == '?' :
                self.maze.curr[x][y] = "f"
                return self.maze.curr
            if self.maze.curr[x][y] == 'f' :
                self.maze.curr[x][y] = "?"
                return self.maze.curr
            
    def translate(self, pos):
        col = math.floor(pos[0]/(CELLSIZE+DIFF))
        row = math.floor(pos[1]/(CELLSIZE+DIFF))
        
        return (row, col)
    