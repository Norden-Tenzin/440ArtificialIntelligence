import numpy as np
import pygame
import os
import sys
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

helper = False

## initializes pygame, creates and returns a screen
def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    
    return screen

def drawBoard(screen, env):
    screen.fill(DARK)
    title = pygame.font.SysFont("ocraextended", 59).render("MINESWEEPER", True, WHITE)
    screen.blit(title, [SIZE, 10])    
    
    for row, line in enumerate(env.getCurr()):
        for col, item in enumerate(line):
            if item == "m":
                pygame.draw.rect(screen, WHITE, (col*CELLSIZE + (col*DIFF) + SIDES, SIDES + row*DIFF + row*CELLSIZE , CELLSIZE, CELLSIZE)) 
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

def drawHelper(screen, env):
    for row, line in enumerate(env.getHelp()):
        for col, item in enumerate(line):
            if env.getCurr()[row][col] == "?":
                if item == "m":
                    pygame.draw.rect(screen, YELLOW, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))
                elif item == "s":
                    pygame.draw.rect(screen, GREEN, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))
            elif env.getCurr()[row][col] == "f":
                if item == "m":
                    pygame.draw.rect(screen, YELLOW, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))
                    flagImage = pygame.image.load(flagPath)
                    screen.blit(flagImage, [((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
                elif item == "s":
                    pygame.draw.rect(screen, GREEN, (((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.85))/2), math.ceil(CELLSIZE*0.85), math.ceil(CELLSIZE*0.85)))
                    flagImage = pygame.image.load(flagPath)
                    screen.blit(flagImage, [((col*CELLSIZE) + (col*DIFF) + SIDES) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2), SIDES + (row*DIFF) + (row*CELLSIZE) + math.ceil((CELLSIZE - math.ceil(CELLSIZE*0.75))/2)])
            
def buttonToggle(bc, ac, screen, env):
    global helper
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect1 = pygame.Rect(SIZE + 5, 80, 284, 50)
    on_button1 = rect1.collidepoint(mouse)
    
    if on_button1 and not helper:  
        pygame.draw.rect(screen, ac, rect1)
        if click[0] == 1:
            helper = True
            pygame.draw.rect(screen, ac, rect1)
            drawHelper(screen, env)
            pygame.time.delay(150)

    elif on_button1 and helper:
        if click[0] == 1:
            helper = False
            pygame.draw.rect(screen, bc, rect1)
            pygame.time.delay(150)
            drawBoard(screen, env)

    elif not on_button1 and helper: 
        pygame.draw.rect(screen, ac, rect1)
    else:
        pygame.draw.rect(screen, bc, rect1)

    helperTxt = pygame.font.SysFont("ocraextended", 35).render("Helper", True, WHITE)
    screen.blit(helperTxt, [SIZE + 10, 85])    

def button(x, y, w, h, bc, ac, screen, env, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    on_button = rect.collidepoint(mouse)
    
    if on_button:
        pygame.draw.rect(screen, ac, rect)
    else:
        pygame.draw.rect(screen, bc, rect)
    if on_button:  
        if click[0] == 1 and action!= None:
            isDead = False
            pathLen = 0
            visitedLen = 0
            algoName = ""
            
            if action == "resetMaze":
                env.resetMaze()
                env.resetHelp()
                drawBoard(screen, env)
                if helper: 
                    drawHelper(screen, env)
            elif action == "newMaze":
                print(helper)
                env.newMaze()
                drawBoard(screen, env)
                if helper: 
                    drawHelper(screen, env)
            pygame.time.delay(100)
    
    newTxt = pygame.font.SysFont("ocraextended", 15).render("New", True, WHITE)
    mazeTxt = pygame.font.SysFont("ocraextended", 15).render("Maze", True, WHITE)
    screen.blit(newTxt, [SIZE + 5 + 284 + 2 + 2, 90])
    screen.blit(mazeTxt, [SIZE + 5 + 284 + 2 + 2, 105])    

    resetTxt = pygame.font.SysFont("ocraextended", 15).render("Reset", True, WHITE)
    screen.blit(resetTxt, [SIZE + 5 + 284 + 2 + 2 + 50 + 1, 90])
    screen.blit(mazeTxt, [SIZE + 5 + 284 + 2 + 2 + 50 + 1, 105])    

def main():
    env = Environment()


    if len(sys.argv) == 1:
        agent = basic_agent(env)
        agent.run()
        # env.resetMaze()
    elif sys.argv[1] == "-ui":
        imageInit()
        screen = initialize()
        drawBoard(screen, env)
        on = True
        while on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on = False
                if event.type == pygame.MOUSEBUTTONDOWN :
                    click = pygame.mouse.get_pressed()
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 2 and pos[0] < SIZE-2) and (pos[1] > 2 and pos[1] < SIZE-2):
                            curr = env.query(pos)
                            agent.runStep()
                        drawBoard(screen, env)
                        if helper: 
                            drawHelper(screen, env)
                            # print(np.array(env.getHelp()))
                    if event.button == 3:
                        pos = pygame.mouse.get_pos()
                        if (pos[0] > 2 and pos[0] < SIZE-2) and (pos[1] > 2 and pos[1] < SIZE-2):
                            curr = env.flag(pos)
                            agent.runStep()
                        drawBoard(screen, env)
                        if helper: 
                            drawHelper(screen, env)
            button(SIZE + 5 + 284 + 2, 80, 50, 50, DARKER, LIGHTDARK, screen, env, "newMaze")
            button(SIZE + 5 + 284 + 50 + 4, 80, 50, 50, DARKER, LIGHTDARK, screen, env, "resetMaze")
            buttonToggle(DARKER, LIGHTDARK, screen, env)
            if helper:
                pygame.draw.circle(screen, GREEN, (SIZE + 270, 105), 4, 0)
            else:
                pygame.draw.circle(screen, RED, (SIZE + 270, 105), 4, 0)
            pygame.display.flip()
if __name__ == "__main__":
    main()