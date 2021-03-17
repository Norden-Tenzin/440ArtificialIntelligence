import numpy as np
import pygame
import os
import math

from image import *
from basic_agent import *
from environment import *
from constants import *
from maze import *

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
smallQuestionPath = os.path.join(THIS_FOLDER, './assets/smallquestion.png')
minePath = os.path.join(THIS_FOLDER, './assets/smallmine.png')

## initializes pygame, creates and returns a screen
def initialize():
    imageInit()
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    return screen

def drawBoard(screen, arr):
    # print(np.array(arr))
    top = 2
    left = 2 # left

    # diff is the border width 

    board = pygame.Surface((SIZE, SIZE))
    screen.fill(DARK)
    
    # for row in range(0, DIM, 1):
    #     for col in range(0, DIM, 1):
    #         pygame.draw.rect(board, WHITE, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        
    print(arr)
    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            # if item == "s":
            #     pygame.draw.rect(board, RED, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))        
            if item == "m":
                pygame.draw.rect(screen, LIGHTDARK, (col*CELLSIZE + (col*DIFF) + left, top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE)) 
                
                mineImage = pygame.image.load(minePath)
                screen.blit(mineImage, [((col*CELLSIZE) + (col*DIFF) + left) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), top + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])       
            elif item == "?":
                pygame.draw.rect(screen, WHITE, (((col*CELLSIZE) + (col*DIFF) + left), top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                
                smallQuestionImage = pygame.image.load(smallQuestionPath)
                screen.blit(smallQuestionImage, [((col*CELLSIZE) + (col*DIFF) + left) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), top + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
            elif item == "f":
                pygame.draw.rect(screen, WHITE, (((col*CELLSIZE) + (col*DIFF) + left), top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                
                smallQuestionImage = pygame.image.load(smallQuestionPath)
                screen.blit(smallQuestionImage, [((col*CELLSIZE) + (col*DIFF) + left) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), top + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
            else:
                pygame.draw.rect(screen, WHITE, (((col*CELLSIZE) + (col*DIFF) + left), top + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                
                textobj = pygame.font.SysFont("ocraextended", math.ceil(CELLSIZE*0.75)).render(item, True, DARKER)
                screen.blit(textobj, [((col*CELLSIZE) + (col*DIFF) + left) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.50))/2), top + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
    # screen.blit(board, board.get_rect())
    
    return board

def main():
    screen = initialize()
    env = Environment()
    
    board = drawBoard(screen, env.getCurr())
    # screen.blit(board, board.get_rect())

    # call basic agent
    # agent = basic_agent(env.getAnswers(), env.getCurr())
    # solving arr with basic agent
    # agent.run()

    # print("~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~")

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                click = pygame.mouse.get_pressed()
                if click[0] == 1:
                    pos = pygame.mouse.get_pos()
                    curr = env.query(pos)
                    
                    board = drawBoard(screen, env.getCurr())
               
            ## FOR KEYPRESSES
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         ## do next move. 
            #         pass 
                
        pygame.display.flip()
                
if __name__ == "__main__":
    main()