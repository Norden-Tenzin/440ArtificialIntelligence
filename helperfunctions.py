import sys
import numpy as np

from constants import *
from main import *

# turns the text into a 2d arr
def readGame():  
    arr = []
    one_line = []
    fixed_line = []
    one_tile = ""

    with open(GAMEFILE, "r") as f:
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
def writeGame(arr, gamefile): 
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

    file = open(gamefile, "w+")
    file.writelines(maze)

def cleanGame():
    file = open(CLEANFILE, "r")
    maze = file.read()
    fileW = open(GAMEFILE, "w+")
    fileW.writelines(maze)

def main():
    arr = mazeMaker(10, 0.3)
    writeGame(arr)
    readGame()

if __name__ ==  "__main__":
    main()