import numpy as np
import pygame
from basic_agent import *
from environment import *
from constants import *
from maze import *


## initializes pygame, creates and returns a screen
def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE , SIZE))
    return screen

def drawBoard(arr):
    print(np.array(arr))
    top = 5
    left = 4 # left

    # diff is the border width 
    diff = 2
    diffn = DIM-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/DIM)

    board = pygame.Surface((SIZE, SIZE))
    board.fill(DARK)
    
    for row in range(0, DIM, 1):
        for col in range(0, DIM, 1):
            pygame.draw.rect(board, WHITE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))        

    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            if item == "s":
                pygame.draw.rect(board, GREEN, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize)) 
            elif item == "m":
                pygame.draw.rect(board, RED, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize)) 
            elif item == "?":
                pygame.draw.rect(board, WHITE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize)) 
    return board

def main():
    screen = initialize()
    maze = Maze()

    board = drawBoard(maze.hidden)
    screen.blit(board, board.get_rect())

    # call basic agent
    agent = basic_agent(maze.shown, maze.hidden)
    # solving arr with basic agent
    agent.run()

    print("~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~")

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ## do next move. 
                    pass 
                
        pygame.display.flip()

if __name__ == "__main__":
    main()