import random
import numpy as np
import math

from constants import *
from mineMap import *

class Environment():
    def __init__(self):
        self.map = MineMap()
        self.boom = 0
        self.found = 0
        
    """

    @arg bool original -
    """
    def newMaze(self):
        self.map = Maze()
    
    def resetMaze(self):
        self.map.resetMaze()
        self.map.resetHelp()
        self.boom = 0
        self.found = 0
    
    def getAnswers(self):
        return self.map.answers
    
    def getCurr(self):
        return self.map.curr
    
    def getHelp(self):
        return self.map.help

    def query(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.map.answers[x][y] != 'm':
                self.map.curr[x][y] = self.map.answers[x][y]
                if self.isGameOver():
                    return True
            else:
                self.boom += 1
                self.map.curr[x][y] = 'm'
                if self.isGameOver():
                    return True
        return False

    def queryAgent(self, pos):
        if self.map.answers[pos[0]][pos[1]] != 'm':
            self.map.curr[pos[0]][pos[1]] = self.map.answers[pos[0]][pos[1]]
        else:
            self.boom += 1
            self.map.curr[pos[0]][pos[1]] = self.map.answers[pos[0]][pos[1]]
            
    def flag(self, pos):
        newPos = self.translate(pos)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            if self.map.curr[x][y] == '?' :
                self.map.curr[x][y] = "f"
                if self.map.answers[x][y] == "m":
                    self.found += 1
                if self.isGameOver():
                    return True
            elif self.map.curr[x][y] == 'f' :
                self.map.curr[x][y] = "?"
                if self.map.answers[x][y] == "m":
                    self.found -= 1
        return False
                    
    def flagAgent(self, pos):
        x = pos[0]
        y = pos[1]
        if self.map.curr[x][y] == '?' :
            self.map.curr[x][y] = "f"
            self.found += 1        

    def isGameOver(self):
        # if all everything is clicked -- bad
        isGameOver = True
        for row, line in enumerate(self.map.curr):
            if "?" in line:
                isGameOver =  False
        # if all mines are cliked it ends -- bad
        # if all mines found it ends -- > if miss then not end. good. 
            for col, item in enumerate(line):
                if self.map.answers[row][col] == "m":
                    if item != "f":
                        isGameOver = False
                elif self.map.answers[row][col] != "m":
                    if item == "?" or item == "f":
                        isGameOver = False
        if self.boom + self.found == NUM_MINES:
            isGameOver = True
        return isGameOver

    def translate(self, pos):
        col = math.floor(pos[0]/(CELLSIZE+DIFF))
        row = math.floor(pos[1]/(CELLSIZE+DIFF))
        return (row, col)
    