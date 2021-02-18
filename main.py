import numpy as np
import random
import pygame
import sys
import Solution

from helperfunctions import *
from constants import *
from Solution import *

strat1 = True
strat2 = False
strat3 = False
position = queue.LifoQueue()

fireStartLoc = (0,0)

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    return screen

def mazeMaker(dim, p):
    finalPath = []

    arr = [['0' for i in range(dim)] for j in range(dim)] 
    arr[0][0] = "s"
    arr[dim-1][dim-1] = "g"

    count = 0
    for row in arr:
        for i, ele in enumerate(row):
            if ele != "s" and ele != "g" and int(ele) == 0:
                if random.randrange(0, 100, 1)/100 < p:
                    row[i] = "x"
                    count += 1

    sol = Solution(arr, (0, 0))
    algoResult = sol.dfs()
    backtrack_info = algoResult[0]
    if backtrack_info != {}:
        finalPath = sol.create_solution(backtrack_info, (0, 0))
    
    if finalPath == []:
        arr = mazeMaker(dim, p)

    writeGame(arr, GAMEFILE)
    writeGame(arr, CLEANFILE)
    writeGame(arr, FIREFILE)
    return arr

def mazePath(visited, finalPath):
    arr = readGame(GAMEFILE)

    for (x, y) in visited:
        if (x, y) != (0, 0) and (x, y) != (len(arr)-1, len(arr)-1):
            arr[x][y] = "1"

    if finalPath != {}:
        for (x, y) in finalPath:
            if (x, y) != (0, 0) and (x, y) != (len(arr)-1, len(arr)-1):
                arr[x][y] = "2"

    writeGame(arr, GAMEFILE)
    return arr

def mazeStep(visited, finalPath, screen):
    arr = readGame(GAMEFILE)
    """
    for (x, y) in visited:
        if (x, y) != (0, 0) and (x, y) != (len(arr)-1, len(arr)-1):
            arr[x][y] = "1"
    """
    if finalPath != {}:
        lst = [ele for ele in reversed(finalPath)] 
        #print(lst[0])
        position.put(lst[0])
        arr[lst[0][0]][lst[0][1]] = "2"

        #---------------------------------------------
        # move writeGame() here
        # To save path in arr
        #---------------------------------------------
        writeGame(arr, GAMEFILE)

    fireTick()
    fireArr = readGame(FIREFILE)
    for i, items in enumerate(fireArr):
        for j, item in enumerate(items):
            if fireArr[i][j] == "f":
                arr[i][j] = "f"

    board = drawBoardArr(MAZE_SIZE, arr)
    screen.blit(board, board.get_rect())
    # update display
    # show the status of maze step by step
    pygame.display.update()

    
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
            elif item == "f":
                pygame.draw.rect(board, YELLOW, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "1":
                pygame.draw.rect(board, LIGHTORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "2":
                pygame.draw.rect(board, ORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
    return board

def drawBoardArr(dim, arr):
    top = 5
    left = 5 # left = lr/2 

    # diff is the border width 
    diff = 2
    diffn = dim-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/dim)

    # arr = readGame(GAMEFILE)
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
            elif item == "f":
                pygame.draw.rect(board, YELLOW, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "1":
                pygame.draw.rect(board, LIGHTORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
            elif item == "2":
                pygame.draw.rect(board, ORANGE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))
    return board

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

# exit functions 
def died(pos):

    (i, j) = pos
    fireArr = readGame(FIREFILE)
    for row, items in enumerate(fireArr):
        for col, item in enumerate(items):
            if (i, j) == (row, col) and item == "f":
                print("died")
                return True
        #-----------------------------------------------
        #  I don't know why but If we use else, player never die
        #  then infinit loop
        #-----------------------------------------------
        """
            else:  
                return False
        """
def escaped(pos):
    if (MAZE_SIZE - 2, MAZE_SIZE - 1) == pos or (MAZE_SIZE - 1, MAZE_SIZE - 2) == pos:
        print("escaped")
        return True
    else:
        return False

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
            if action == "rerollMAZE":
                cleanGame()
                arr = mazeMaker(MAZE_SIZE, 0.3)
                fireStart()
                fireArr = readGame(FIREFILE)
                for i, items in enumerate(fireArr):
                    for j, item in enumerate(items):
                        if fireArr[i][j] == "f":
                            arr[i][j] = "f"

                board = drawBoardArr(MAZE_SIZE, arr)
                screen.blit(board, board.get_rect())
                pygame.time.delay(100)

            elif action == "rerollFIRE":
                cleanGame()
                fireStart()
                arr = readGame(GAMEFILE)
                fireArr = readGame(FIREFILE)
                for i, items in enumerate(fireArr):
                    for j, item in enumerate(items):
                        if fireArr[i][j] == "f":
                            arr[i][j] = "f"
                board = drawBoardArr(MAZE_SIZE, arr)
                screen.blit(board, board.get_rect())
                pygame.time.delay(100)

def buttonToggle(ic, ac, screen, action=None):
    global strat1
    global strat2
    global strat3

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect1 = pygame.Rect(SIZE + 5, 195, 121, 50)
    rect2 = pygame.Rect(SIZE + 5 + 121 + 10, 195, 121, 50)
    rect3 = pygame.Rect(SIZE + 5 + 242 + 20, 195, 121, 50)

    on_button1 = rect1.collidepoint(mouse)
    on_button2 = rect2.collidepoint(mouse)
    on_button3 = rect3.collidepoint(mouse)

    if on_button1:  
        pygame.draw.rect(screen, ac, rect1)
        if click[0] == 1:
            if strat1:
                strat1 = False
                pygame.draw.rect(screen, ac, rect1)
            else:
                strat1 = True
                strat2 = False
                strat3 = False
                pygame.draw.rect(screen, ic, rect1)
            pygame.time.delay(100)
    elif not on_button1 and strat1: 
        pygame.draw.rect(screen, ac, rect1)
    else:
        pygame.draw.rect(screen, ic, rect1)

    if on_button2:  
        pygame.draw.rect(screen, ac, rect2)
        if click[0] == 1:
            if strat2:
                strat2 = False
                pygame.draw.rect(screen, ac, rect2)
            else:
                strat1 = False
                strat2 = True
                strat3 = False
                pygame.draw.rect(screen, ic, rect2)
            pygame.time.delay(100)
    elif not on_button2 and strat2: 
        pygame.draw.rect(screen, ac, rect2)
    else:
        pygame.draw.rect(screen, ic, rect2)

    if on_button3:  
        pygame.draw.rect(screen, ac, rect3)
        if click[0] == 1:
            if strat3:
                strat3 = False
                pygame.draw.rect(screen, ac, rect3)
            else:
                strat1 = False
                strat2 = False
                strat3 = True
                pygame.draw.rect(screen, ic, rect3)
            pygame.time.delay(100)
    elif not on_button3 and strat3: 
        pygame.draw.rect(screen, ac, rect3)
    else:
        pygame.draw.rect(screen, ic, rect3)

    draw_text('STRAT1', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 5, 205)
    draw_text('STRAT2', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 5, 205)
    draw_text('STRAT3', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 10, 205)

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
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, GAMEFILE)
                writeGame(arr, FIREFILE)

                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())
                pygame.time.delay(100)

            elif action == "dfs" and strat1:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.dfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))

                for i, position in enumerate([ele for ele in reversed(finalPath)]):
                    arr[position[0]][position[1]] = "2"
                    fireTick()
                    writeGame(arr, GAMEFILE)
                    fireArr = readGame(FIREFILE)

                    for i, items in enumerate(fireArr):
                        for j, item in enumerate(items):
                            if fireArr[i][j] == "f":
                                arr[i][j] = "f"

                    board = drawBoardArr(MAZE_SIZE, arr)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()

                    if escaped(position) or died(position):
                        break
                    pygame.time.delay(10)
                pygame.time.delay(100)

            elif action == "bfs" and strat1:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.bfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))

                for i, position in enumerate([ele for ele in reversed(finalPath)]):
                    arr[position[0]][position[1]] = "2"
                    fireTick()
                    writeGame(arr, GAMEFILE)
                    fireArr = readGame(FIREFILE)

                    for i, items in enumerate(fireArr):
                        for j, item in enumerate(items):
                            if fireArr[i][j] == "f":
                                arr[i][j] = "f"

                    board = drawBoardArr(MAZE_SIZE, arr)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()

                    if escaped(position) or died(position):
                        break
                    pygame.time.delay(10)
                pygame.time.delay(100)

            elif action == "a*" and strat1:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.a_star()
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))

                for i, position in enumerate([ele for ele in reversed(finalPath)]):
                    arr[position[0]][position[1]] = "2"
                    fireTick()
                    writeGame(arr, GAMEFILE)
                    fireArr = readGame(FIREFILE)

                    for i, items in enumerate(fireArr):
                        for j, item in enumerate(items):
                            if fireArr[i][j] == "f":
                                arr[i][j] = "f"

                    board = drawBoardArr(MAZE_SIZE, arr)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()

                    if escaped(position) or died(position):
                        break
                    pygame.time.delay(10)
                pygame.time.delay(100)

            elif action == "dfs" and strat2:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.dfs()
           
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    print(pos)
                    #--------------------------------------
                    # Remove "1" before send it to solution
                    # The reason is written below
                    #--------------------------------------
                    """
                    for i in range(0, MAZE_SIZE, 1):
                        for j in range(0, MAZE_SIZE, 1):
                            if arr[i][j] == "1":
                                arr[i][j] = '0'
                    """
                    sol = Solution(arr, pos)
                    algoResult = sol.dfs()
                    #--------------------------------------
                    # backtrack_info is empty
                    # we edit arr in mazeStep(add 1 or 2 as value)
                    # find_neighbor() picks block only with "0" or "g"
                    # no neighbor -> no route
                    # a_star() returns ({}, visited)
                    #---------------------------------------
                    #print(algoResult)
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    #print(backtrack_info)
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                        #print(finalPath)
                    if escaped(pos) or died(pos):
                        notComplete = False
                pygame.time.delay(1000)

            elif action == "bfs" and strat2:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.bfs()
           
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    print(pos)
                    #--------------------------------------
                    # Remove "1" before send it to solution
                    # The reason is written below
                    #--------------------------------------
                    """
                    for i in range(0, MAZE_SIZE, 1):
                        for j in range(0, MAZE_SIZE, 1):
                            if arr[i][j] == "1":
                                arr[i][j] = '0'
                    """
                    sol = Solution(arr, pos)
                    algoResult = sol.bfs()
                    #--------------------------------------
                    # backtrack_info is empty
                    # we edit arr in mazeStep(add 1 or 2 as value)
                    # find_neighbor() picks block only with "0" or "g"
                    # no neighbor -> no route
                    # a_star() returns ({}, visited)
                    #---------------------------------------
                    #print(algoResult)
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    #print(backtrack_info)
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                        #print(finalPath)
                    if escaped(pos) or died(pos):
                        notComplete = False
                pygame.time.delay(1000)

            elif action == "a*" and strat2:
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)

                finalPath = {}
                sol = Solution(arr, (0, 0))
                algoResult = sol.a_star()
           
                backtrack_info = algoResult[0]
                visited = algoResult[1]

                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    print(pos)
                    #--------------------------------------
                    # Remove "1" before send it to solution
                    # The reason is written below
                    #--------------------------------------
                    """
                    for i in range(0, MAZE_SIZE, 1):
                        for j in range(0, MAZE_SIZE, 1):
                            if arr[i][j] == "1":
                                arr[i][j] = '0'
                    """
                    sol = Solution(arr, pos)
                    algoResult = sol.a_star()
                    #--------------------------------------
                    # backtrack_info is empty
                    # we edit arr in mazeStep(add 1 or 2 as value)
                    # find_neighbor() picks block only with "0" or "g"
                    # no neighbor -> no route
                    # a_star() returns ({}, visited)
                    #---------------------------------------
                    #print(algoResult)
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    #print(backtrack_info)
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                        #print(finalPath)
                    if escaped(pos) or died(pos):
                        notComplete = False
                pygame.time.delay(1000)
            
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def isComplete(screen):
    arr = readGame(GAMEFILE)
    if arr[(len(arr)-2)][(len(arr)-1)] == "2" or arr[(len(arr)-1)][(len(arr)-2)] == "2":
        draw_text('True', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 170, 250)
    else:
        draw_text('False', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 170, 250)

def main():
    screen = initialize()
    arr = mazeMaker(MAZE_SIZE, 0.3)
    fireStart()

    fireArr = readGame(FIREFILE)
    for i, items in enumerate(fireArr):
        for j, item in enumerate(items):
            if fireArr[i][j] == "f":
                arr[i][j] = "f"

    board = drawBoardArr(MAZE_SIZE, arr)
    screen.blit(board, board.get_rect())

    # fireTick()
    # fireTick()

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False

        draw_text('MAZE ON FIRE', pygame.font.SysFont("ocraextended", 50), (255, 255, 255), screen, SIZE + 20, 10)
        dice = pygame.image.load('./assets/dice2.png').convert_alpha()
        fire = pygame.image.load('./assets/smallfire.png').convert_alpha()

        button(SIZE + 168, 75, 100, 50, DARKER, LIGHTDARK, screen, "clear")
        buttonImage(SIZE + 278, 75, 50, 50, DARKER, LIGHTDARK, dice, dice, screen, "rerollMAZE") #rerolls the maze and the fire.
        buttonImage(SIZE + 338, 75, 50, 50, DARKER, LIGHTDARK, fire, fire, screen, "rerollFIRE") #rerolls the fire.

        button(SIZE + 5, 135, 121, 50, DARKER, LIGHTDARK, screen, "dfs")
        button(SIZE + 5 + 121 + 10, 135, 121, 50, DARKER, LIGHTDARK, screen, "bfs")
        button(SIZE + 5 + 242 + 20, 135, 121, 50, DARKER, LIGHTDARK, screen, "a*")

        # button(SIZE + 5, 195, 186, 50, DARKER, LIGHTDARK, screen, "strat1")
        # button(SIZE + 5 + 186 + 10, 195, 187, 50, DARKER, LIGHTDARK, screen, "strat2")

        buttonToggle(DARKER, LIGHTDARK, screen)

        draw_text('Clear', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 168 + 5, 82)
        draw_text('DFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 30, 142)
        draw_text('BFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 30, 142)
        draw_text('A*', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 40, 142)
        draw_text('STRAT1', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 5, 205)
        draw_text('STRAT2', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 5, 205)
        draw_text('STRAT3', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 10, 205)
        draw_text('Maze Escaped:', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 250)
        isComplete(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()