import numpy as np
import random
import pygame
import sys
import Solution

from helperfunctions import *
from constants import *
from Solution import *

fireStartLoc = (0,0)

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
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
    
    writeGame(arr, GAMEFILE)
    writeGame(arr, CLEANFILE)
    writeGame(arr, FIREFILE)

    return arr

def mazePath(visited, finalPath):
    arr = readGame()

    for (x, y) in visited:
        if (x, y) != (0, 0) and (x, y) != (99, 99):
            arr[x][y] = "1"

    if finalPath != {}:
        for (x, y) in finalPath:
            if (x, y) != (0, 0) and (x, y) != (99, 99):
                arr[x][y] = "2"
    writeGame(arr, GAMEFILE)
    return arr

def drawBoard(dim):
    top = 5
    left = 5 # left = lr/2 

    # diff is the border width 
    diff = 2
    diffn = dim-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/dim)

    arr = readGame(GAMEFILE)
    board = pygame.Surface((SIZE + UI_SPACE, SIZE))
    board.fill(DARK)
    
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

def fireStart():
    arr = readGame(FIREFILE)
    row = random.randrange(0, MAZE_SIZE, 1)
    col = random.randrange(0, MAZE_SIZE, 1)
    if arr[row][col] == "0":
        arr[row][col] = "f"
        fireStartLoc = (row, col)
        writeGame(arr, FIREFILE)
    else:
        fireStart()

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
        if random.random() <= prob:
            arr[i][j] = "f"
    writeGame(arr, FIREFILE)

def buttonImage(x, y, w, h, ic, ac, img, imgon, screen, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)
    on_button = rect.collidepoint(mouse)
    if on_button:
        pygame.draw.rect(screen, ac, rect)
        screen.blit(imgon, imgon.get_rect(center = rect.center))
    else:
        pygame.draw.rect(screen, ic, rect)
        screen.blit(img, img.get_rect(center = rect.center))

    if on_button:  
        if click[0] == 1 and action!= None:
            if action == "reroll":
                cleanGame()
                mazeMaker(MAZE_SIZE, 0.3)
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())

def button(x, y, w, h, ic, ac, screen, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)
    on_button = rect.collidepoint(mouse)
    if on_button:
        pygame.draw.rect(screen, ac, rect)
    else:
        pygame.draw.rect(screen, ic, rect)

    if on_button:  
        if click[0] == 1 and action!= None:
            if action == "clear":
                cleanGame()
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())
                
            elif action == "dfs":
                cleanGame()
                arr = readGame()
                finalPath = {}
                sol = Solution(arr)
                algoResult = sol.dfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info)

                arr = mazePath(visited, finalPath)
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())

            elif action == "bfs":
                cleanGame()
                arr = readGame()
                finalPath = {}
                sol = Solution(arr)
                algoResult = sol.bfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info)

                arr = mazePath(visited, finalPath)
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())

            elif action == "a*":
                cleanGame()
                arr = readGame()
                finalPath = {}
                sol = Solution(arr)
                algoResult = sol.a_star()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info)

                arr = mazePath(visited, finalPath)
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def isComplete(screen):
    arr = readGame(GAMEFILE)
    if arr[(len(arr)-2)][(len(arr)-1)] == "2" or arr[(len(arr)-1)][(len(arr)-2)] == "2":
        draw_text('True', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 200, 190)
    else:
        draw_text('False', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 170, 190)

def main():
    screen = initialize()
    arr = mazeMaker(MAZE_SIZE, 0.3)
    board = drawBoard(MAZE_SIZE)
    screen.blit(board, board.get_rect())

    fireStart()
    fireTick()
    # fireTick()

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False

        draw_text('MAZE ON FIRE', pygame.font.SysFont("ocraextended", 50), (255, 255, 255), screen, SIZE + 20, 10)
        image = pygame.image.load('./assets/dice2.png').convert_alpha()
        button(SIZE + 228, 75, 100, 50, DARKER, LIGHTDARK, screen, "clear")
        buttonImage(SIZE + 338, 75, 50, 50, DARKER, LIGHTDARK, image, image, screen, "reroll")
        button(SIZE + 5, 135, 121, 50, DARKER, LIGHTDARK, screen, "dfs")
        button(SIZE + 5 + 121 + 10, 135, 121, 50, DARKER, LIGHTDARK, screen, "bfs")
        button(SIZE + 5 + 242 + 20, 135, 121, 50, DARKER, LIGHTDARK, screen, "a*")

        draw_text('Clear', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 228 + 5, 82)
        draw_text('DFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 30, 142)
        draw_text('BFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 30, 142)
        draw_text('A*', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 40, 142)
        draw_text('Maze Escaped:', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 190)
        isComplete(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()