import numpy as np
import random
import pygame
import Solution

from helperfunctions import *
from constants import *
from Solution import *

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    return screen

def mazeMaker(dim, p):
    arr = [['0' for i in range(dim)] for j in range(dim)] 
    arr[0][0] = "s"
    arr[dim-1][dim-1] = "g"

    count = 0
    for row in arr:
        for i, ele in enumerate(row):
            if ele != "s" and ele != "g" and int(ele) == 0:
                if random.randrange(0, 100, 1)/100 < p:
                    # print("here")
                    row[i] = "x"
                    count += 1
    
    writeGame(arr)
    return arr



def mazePath(visited, finalPath):
    arr = readGame()

    for (x, y) in visited:
        if (x, y) != (0, 0) and (x, y) != (99, 99):
            arr[x][y] = "1"
    for (x, y) in finalPath:
        if (x, y) != (0, 0) and (x, y) != (99, 99):
            arr[x][y] = "2"
    writeGame(arr)
    return arr
    

def drawBoard(dim):
    top = 5
    left = 5 # left = lr/2 

    # diff is the border width 
    diff = 2
    diffn = dim-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/dim)

    arr = readGame()
    board = pygame.Surface((SIZE, SIZE))
    board.fill((DARK))
    
    for row in range(0, dim, 1):
        for col in range(0, dim, 1):
            pygame.draw.rect(board, WHITE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))        

    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            if item == "s" or item == "g":
                pygame.draw.rect(board, GREEN, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize)) 
            elif item == "x":
                pygame.draw.rect(board, BLACK, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "1":
                pygame.draw.rect(board, LIGHTORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "2":
                pygame.draw.rect(board, ORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))

    return board

def draw(dim, cord, blockType):
    # player, block and fire 
    #cord is a tuple
    #example cord 0,1 
    top = 5
    left = 5 # left = lr/2 

    # diff is the border width 
    diff = 2
    diffn = dim-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/dim)

    board = drawBoard(dim)

    if(blockType == "agent"):
        pygame.draw.rect(board, RED, (cord[1]*cellSize + (cord[1]+1)*diff + left, top + cord[0]*diff + cord[0]*cellSize , cellSize, cellSize))        

    # if(blockType == "block"):
    # if(blockType == "fire"):
    return board

def main():
    size = 100
    screen = initialize()
    arr = mazeMaker(size, 0.3)
    
    sol = Solution(arr)
    algoResult = sol.a_star()
    backtrack_info = algoResult[0]
    visited = algoResult[1]
    finalPath = sol.create_solution(backtrack_info)  
    if finalPath:
        arr = mazePath(visited, finalPath)
    # print(len(x))
    # print(x)

    board = drawBoard(size)

    screen.blit(board, board.get_rect())

    # sol = Solution.Solution(arr)
    # sol.dfs()
    # sol.bfs()
    # sol.a_star()

    
    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.flip()

if __name__ == "__main__":
    main()