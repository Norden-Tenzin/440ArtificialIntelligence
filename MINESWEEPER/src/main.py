import numpy as np
import pygame
import os
import math

from image import *
from basic_agent import *
from advanced_agent import *
from environment import *
from constants import *
from maze import *

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
smallQuestionPath = os.path.join(THIS_FOLDER, './assets/smallquestion.png')
minePath = os.path.join(THIS_FOLDER, './assets/smallmine.png')
flagPath = os.path.join(THIS_FOLDER, './assets/smallflag.png')

## initializes pygame, creates and returns a screen
def initialize():
    imageInit()
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    return screen

def drawBoard(screen, arr):
    board = pygame.Surface((SIZE, SIZE))
    screen.fill(DARK)
         
    print(arr)
    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            if item == "m":
                pygame.draw.rect(screen, LIGHTDARK, (col*CELLSIZE + (col*DIFF) + SIDES, SIDES + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE)) 
                
                mineImage = pygame.image.load(minePath)
                screen.blit(mineImage, [((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])       
            
            elif item == "?":
                pygame.draw.rect(screen, DARKER, (((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                pygame.draw.polygon(screen, WHITE, [(((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + (row*DIFF) + (row*CELLSIZE)), (((col*CELLSIZE) + (col*DIFF) + SIDES + CELLSIZE -1), SIDES + (row*DIFF) + (row*CELLSIZE)), (((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + (row*DIFF) + (row*CELLSIZE) + CELLSIZE -1)])
                pygame.draw.rect(screen, LIGHTDARK, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))

            elif item == "f":
                pygame.draw.rect(screen, DARKER, (((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                pygame.draw.polygon(screen, WHITE, [(((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + (row*DIFF) + (row*CELLSIZE)), (((col*CELLSIZE) + (col*DIFF) + SIDES + CELLSIZE -1), SIDES + (row*DIFF) + (row*CELLSIZE)), (((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + (row*DIFF) + (row*CELLSIZE) + CELLSIZE -1)])
                pygame.draw.rect(screen, LIGHTDARK, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))
                
                flagImage = pygame.image.load(flagPath)
                screen.blit(flagImage, [((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
            
            else:
                pygame.draw.rect(screen, WHITE, (((col*CELLSIZE) + (col*DIFF) + SIDES), SIDES + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE))
                color = DARKER
                if item == "1":
                    color = NUMBER1
                elif item == "2":
                    color = NUMBER2
                elif item == "3":
                    color = NUMBER3
                elif item == "4":
                    color = NUMBER4
                elif item == "5":
                    color = NUMBER5
                elif item == "6":
                    color = NUMBER6
                elif item == "7":
                    color = NUMBER7
                elif item == "8":
                    color = NUMBER8
                    
                if item != "0":
                    textobj = pygame.font.SysFont("ocraextended", math.ceil(CELLSIZE*0.75)).render(item, True, color)
                    screen.blit(textobj, [((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.50))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])    
    return board

def main():
    screen = initialize()
    env = Environment()
    m = Maze()
    
    board = drawBoard(screen, env.getCurr())
    # screen.blit(board, board.get_rect())

    # # call basic agent
    # agent = basic_agent(env.getAnswers(), env.getCurr())
    # agent1 = Advanced_agent(env.getAnswers(), m.emptyFieldMaker())
    # # solving arr with basic agent
    # agent.run()
    # agent1.run()

    # print("~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~")

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                click = pygame.mouse.get_pressed()
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 2 and pos[0] < SIZE-2:
                        curr = env.query(pos)
                    else: 
                        print("NOCLICK")
                    board = drawBoard(screen, env.getCurr())
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 2 and pos[0] < SIZE:
                        curr = env.flag(pos)
                    
                    board = drawBoard(screen, env.getCurr())
               
            ## FOR KEYPRESSES
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         ## do next move. 
            #         pass 
        pygame.display.flip()
                
if __name__ == "__main__":
    main()