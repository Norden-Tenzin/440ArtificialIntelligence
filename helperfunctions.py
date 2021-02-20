## @Sangkyun Kim @Tenzin Norden
## PROJECT 1 440 

## imports
import sys
import numpy as np
from constants import *

## Reads the text file into a 2d array
## @param fileName its the file name used to open and read the file
## @return arr holds the maze from the givern file 
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

## Writes the 2d arrayy into a text file
## @param fileName its the file name used to write into the file
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

## CleanGame Reads from CLEANFILE and writes into GAMEFILE AND FIREFILE
def cleanGame():
    file = open(CLEANFILE, "r")
    maze = file.read()
    fileG = open(GAMEFILE, "w+")
    fileG.writelines(maze)
    fileF = open(FIREFILE, "w+")
    fileF.writelines(maze)