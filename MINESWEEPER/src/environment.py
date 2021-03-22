import random
import numpy as np
import math

from constants import *
from maze import *

class Environment():
    def __init__(self):
        self.maze = Maze()
        self.boom = 0
        self.found = 0
    """

        @arg bool original -
    """
    def newMaze(self):
        self.maze = Maze()
    
    def resetMaze(self):
        self.maze.resetMaze()
        self.maze.resetHelp()
        self.boom = 0
        self.found = 0
    
    def getAnswers(self):
        return self.maze.answers
    
    def getCurr(self):
        return self.maze.curr
    
    def getHelp(self):
        return self.maze.help

    def query(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.maze.answers[x][y] != 'm':
                self.maze.curr[x][y] = self.maze.answers[x][y]
                return self.maze.curr
            else:
                self.maze.curr[x][y] = 'm'
                return self.maze.curr

    def queryAgent(self, pos):
        if self.maze.answers[pos[0]][pos[1]] != 'm':
            self.maze.curr[pos[0]][pos[1]] = self.maze.answers[pos[0]][pos[1]]
        else:
            self.boom += 1
            self.maze.curr[pos[0]][pos[1]] = self.maze.answers[pos[0]][pos[1]]
            
    def flag(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.maze.curr[x][y] == '?' :
                self.maze.curr[x][y] = "F"
                return self.maze.curr
            if self.maze.curr[x][y] == 'F' :
                self.maze.curr[x][y] = "?"
                return self.maze.curr
    
    def flagAgent(self, pos):
        x = pos[0]
        y = pos[1]
        if self.maze.curr[x][y] == '?' :
            self.maze.curr[x][y] = "f"
            self.found += 1        

    def translate(self, pos):
        col = math.floor(pos[0]/(CELLSIZE+DIFF))
        row = math.floor(pos[1]/(CELLSIZE+DIFF))
        return (row, col)
    