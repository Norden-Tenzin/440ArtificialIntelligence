import sys
import numpy as np

from constants import *
from main import *

# turns the text into a 2d arr
def readGame(fileName):  
    arr = []
    one_line = []
    fixed_line = []
    one_tile = ""

    with open(fileName, "r") as f:
        game_map = f.readlines()
    game_map = [line.strip() for line in game_map]

    for line in game_map:
        one_line = line.split(",")
        for item in one_line:
            fixed_line.append(item.strip()) 
        arr.append(fixed_line)
        one_line = []
        fixed_line = []
    return arr

# turns 2d arr to text
def writeGame(arr, fileName): 
    maze = []
    one_line = ""
    locationholder = ""
    output = ""
    empty = "##"

    for i, line in  enumerate(arr):
        for j, item in enumerate(line):
            one_line += item + ", "
        one_line = one_line[:-2]
        maze.append(one_line + "\n")
        # print(one_line)
        one_line = ""

    file = open(fileName, "w+")
    file.writelines(maze)

def cleanGame():
    file = open(CLEANFILE, "r")
    maze = file.read()
    fileG = open(GAMEFILE, "w+")
    fileG.writelines(maze)
    fileF = open(FIREFILE, "w+")
    fileF.writelines(maze)

# FIRE
def fireStart():
    global fireStartLoc
    arr = readGame(GAMEFILE)

    notFound = True
    while notFound:
        row = random.randrange(0, MAZE_SIZE, 1)
        col = random.randrange(0, MAZE_SIZE, 1)
        if arr[row][col] == "0":
            arr[row][col] = "f"
            fireStartLoc = (row, col)
            notFound = False
    writeGame(arr, FIREFILE)

def neighborOnFire(row, col, arr):
    neighbor = [(row, col + 1), (row - 1, col), (row, col - 1), (row + 1, col)]
    for (i, j) in neighbor:
        if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
            if arr[i][j] == "f":
                return True
    return False

def fireTick():
    mazeNeighbors = []
    arr = readGame(FIREFILE)
    k = 0

    for row, items in enumerate(arr):
        for col, item in enumerate(items):
            if item == "0" and neighborOnFire(row, col, arr):
                mazeNeighbors.append((row,col))
                k += 1

    prob = 1 - pow((1 - Q), k)
    for (i, j) in mazeNeighbors:
        # I edit this line to use small number of Q (0.1 or 0.3)
        if random.randrange(0, 100, 1)/100 <= prob:
            arr[i][j] = "f"
    writeGame(arr, FIREFILE)

def main():
    arr = mazeMaker(10, 0.3)
    writeGame(arr)
    readGame()

if __name__ ==  "__main__":
    main()