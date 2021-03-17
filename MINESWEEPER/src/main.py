import numpy as np
import pygame
from basic_agent import *
from advanced_agent import *
from environment import *
from constants import *
from maze import *


## initializes pygame, creates and returns a screen
def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    return screen

def drawBoard(arr):
    print(np.array(arr))
    top = 5
    left = 5 # left

    # diff is the border width 

    board = pygame.Surface((SIZE, SIZE))
    board.fill(DARK)
    
    for row in range(0, DIM, 1):
        for col in range(0, DIM, 1):
            pygame.draw.rect(board, WHITE, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        

    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            # if item == "s":
            #     pygame.draw.rect(board, RED, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        
            if item == "m":
                pygame.draw.rect(board, BLACK, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        
            elif item == "?":
                pygame.draw.rect(board, WHITE, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        
    return board

def main():
    screen = initialize()
    env = Environment()
    m = Maze()
    
    board = drawBoard(env.getCurr())
    screen.blit(board, board.get_rect())

    # call basic agent
    agent = basic_agent(env.getAnswers(), env.getCurr())
    agent1 = Advanced_agent(env.getAnswers(), m.emptyFieldMaker())
    # solving arr with basic agent
    agent.run()
    agent1.run()

    print("~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~")

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                curr = env.query(pos)
                
                board = drawBoard(env.getCurr())
                screen.blit(board, board.get_rect())
               
            ## FOR KEYPRESSES
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         ## do next move. 
            #         pass 
                
        pygame.display.flip()
                
if __name__ == "__main__":
    main()