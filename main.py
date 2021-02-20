## @Sangkyun Kim @Tenzin Norden
## PROJECT 1 440 

## imports
import numpy as np
import random
import pygame
import sys
import Solution
from helperfunctions import *
from constants import *
from Solution import *

## global variables 
strat1 = True
strat2 = False
strat3 = False

isfireOn = True
stepPrint = True

isDead = False
pathLen = 0
visitedLen = 0
algoName = ""
position = queue.LifoQueue()
fireStartLoc = (0,0)

count = 0


## initializes pygame, creates and returns a screen
def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE + UI_SPACE, SIZE))
    return screen

## Makes a maze array of size dim x dim
## @param dim is the dimentions of the maze
## @param p is probablity of obstacles
## @return arr - the maze array 
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

    sol = Solution(arr, (0, 0), "strat1", fireStartLoc)
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

## Draws a path with the given visited and finalPath and writes it into GAMEFILE
## @param visited it holds the pos of all the visited blocks
## @param finalPath it holds the pos of all the blocks on the final path
def mazePath(visited, finalPath):
    global visitedLen
    global pathLen

    arr = readGame(GAMEFILE)
    for i, (x, y) in enumerate(visited):
        if arr[x][y] ==  "0":
            arr[x][y]  =  "1"

    if finalPath != {}:
        for i, (x, y) in enumerate([ele for ele in reversed(finalPath)] ):
            if (x, y) != (0, 0) and (x, y) != (len(arr)-1, len(arr)-1):
                arr[x][y] = "2"
                fireTick()
                fireArr = readGame(FIREFILE)
                for i, items in enumerate(fireArr):
                    for j, item in enumerate(items):
                        if fireArr[i][j] == "f":
                            arr[i][j] = "f"

                pathLen += 1
                if escaped((x,y)) or died((x,y)):
                    visitedLen = len(visited)
                    break
    writeGame(arr, GAMEFILE)

## Draws a path step by step with the given visited and finalPath and displays it to screen
## @param visited it holds the pos of all the visited blocks
## @param finalPath it holds the pos of all the blocks on the final path
## @param screen display surface
## @return arr - edited the maze array 
def mazeStep(visited, finalPath, screen):
    arr = readGame(GAMEFILE)

    if finalPath != {}:
        lst = [ele for ele in reversed(finalPath)] 
        position.put(lst[0])
        arr[lst[0][0]][lst[0][1]] = "2"
        writeGame(arr, GAMEFILE)

    fireTick()
    fireArr = readGame(FIREFILE)
    for i, items in enumerate(fireArr):
        for j, item in enumerate(items):
            if fireArr[i][j] == "f":
                arr[i][j] = "f"
    
    board = drawBoardArr(MAZE_SIZE, arr)
    screen.blit(board, board.get_rect())
    pygame.display.flip()
    return arr

## Displays the maze from the GAMEFILE
## @param dim is the dimentions of the maze
## @return board - pygame surface
def drawBoard(dim):
    top = 5
    left = 5 # left

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

## Displays the maze from the arr
## @param dim is the dimentions of the maze
## @param arr is edited GAMEFILE array
## @return board - pygame surface
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

## Creates a fire block randomly on the map and writes it into FIREFILE
def fireStart():
    global fireStartLoc

    if isfireOn:
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

## Finds if the given row and col in arr is neigboring a fire block
## @return if it is neighboring a fire block return True else False
def neighborOnFire(row, col, arr):
    neighbor = [(row, col + 1), (row - 1, col), (row, col - 1), (row + 1, col)]
    for (i, j) in neighbor:
        if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
            if arr[i][j] == "f":
                return True
    return False

## Runs the fire spread probability and spreads it once then writes that into FIREFILE
def fireTick():
    global count 
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
        if random.randrange(0, 100, 1)/100 <= prob:
            arr[i][j] = "f"
    count += 1
    writeGame(arr, FIREFILE)

## Checks if fire block exists on the given pos
## @return if it does then return True otherwise False
def died(pos):
    global isDead 

    (i, j) = pos
    fireArr = readGame(FIREFILE)
    for row, items in enumerate(fireArr):
        for col, item in enumerate(items):
            if (i, j) == (row, col) and item == "f":
                isDead = True
                return True
    return False

## Checks if the given pos is next to exit block
## @return if it is then return True otherwise False
def escaped(pos):
    if (MAZE_SIZE - 2, MAZE_SIZE - 1) == pos or (MAZE_SIZE - 1, MAZE_SIZE - 2) == pos:
        return True
    return False

## Creats a button with an image and displays it on the screen
## @param x is the x position of the rect on the screen
## @param y is the y position of the rect on the screen
## @param w is the width of the rect on the screen
## @param h is the height of the rect on the screen
## @param ic is the color on the screen before the mouse hovers
## @param ac is the color on the screen while the mouse hovers
## @param img is the image on the screen before the mouse hovers
## @param imgon is the image on the screen while the mouse hovers
## @param screen display surface
## @param action tell the funtion which functions to execute
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
        isDead = False
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

## Creats a Toggleable button and displays it on the screen
## @param ic is the color on the screen before the mouse hovers
## @param ac is the color on the screen while the mouse hovers
## @param screen display surface
## @param action tell the funtion which functions to execute
def buttonToggle(ic, ac, screen, action=None):
    global strat1
    global strat2
    global strat3
    global isfireOn 
    global stepPrint

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect1 = pygame.Rect(SIZE + 5, 135, 121, 50)
    rect2 = pygame.Rect(SIZE + 5 + 121 + 10, 135, 121, 50)
    rect3 = pygame.Rect(SIZE + 5 + 242 + 20, 135, 121, 50)

    smallfire = pygame.image.load('./assets/smallfire.png').convert_alpha()
    rect4 = pygame.Rect(SIZE + 338, 75, 50, 50)
   
    smallsteps = pygame.image.load('./assets/smallsteps.png').convert_alpha()
    rect5 = pygame.Rect(SIZE + 5, 75, 93, 50)

    on_button1 = rect1.collidepoint(mouse)
    on_button2 = rect2.collidepoint(mouse)
    on_button3 = rect3.collidepoint(mouse)
    on_button4 = rect4.collidepoint(mouse)
    on_button5 = rect5.collidepoint(mouse)
    
    if on_button1:  
        pygame.draw.rect(screen, ac, rect1)
        if click[0] == 1:
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
            strat1 = False
            strat2 = False
            strat3 = True
            pygame.draw.rect(screen, ic, rect3)
            pygame.time.delay(100)
    elif not on_button3 and strat3: 
        pygame.draw.rect(screen, ac, rect3)
    else:
        pygame.draw.rect(screen, ic, rect3)

    if on_button4:  
        pygame.draw.rect(screen, ac, rect4)
        screen.blit(smallfire, smallfire.get_rect(center = rect4.center))
        if click[0] == 1:
            if isfireOn:
                isfireOn = False
                cleanGame()
                # pygame.display.update()
                board = drawBoard(MAZE_SIZE)
                screen.blit(board, board.get_rect())

                pygame.draw.rect(screen, ac, rect4)
                screen.blit(smallfire, smallfire.get_rect(center = rect4.center))
            else:
                isfireOn = True
                fireStart()
                arr = readGame(GAMEFILE)
                fireArr = readGame(FIREFILE)
                for i, items in enumerate(fireArr):
                    for j, item in enumerate(items):
                        if fireArr[i][j] == "f":
                            arr[i][j] = "f"

                board = drawBoardArr(MAZE_SIZE, arr)
                screen.blit(board, board.get_rect())
                pygame.draw.rect(screen, ic, rect4)
                screen.blit(smallfire, smallfire.get_rect(center = rect4.center))
            pygame.time.delay(100)
    elif not on_button4 and isfireOn: 
        pygame.draw.rect(screen, ac, rect4)
        screen.blit(smallfire, smallfire.get_rect(center = rect4.center))
    else:
        pygame.draw.rect(screen, ic, rect4)
        screen.blit(smallfire, smallfire.get_rect(center = rect4.center))

    if on_button5:  
        pygame.draw.rect(screen, ac, rect5)
        screen.blit(smallsteps, smallsteps.get_rect(center = rect5.center))
        if click[0] == 1:
            if stepPrint:
                stepPrint = False

                pygame.draw.rect(screen, ac, rect5)
                screen.blit(smallsteps, smallsteps.get_rect(center = rect5.center))
            else:
                stepPrint = True
                
                pygame.draw.rect(screen, ic, rect5)
                screen.blit(smallsteps, smallsteps.get_rect(center = rect5.center))
            pygame.time.delay(100)
    elif not on_button5 and stepPrint: 
        pygame.draw.rect(screen, ac, rect5)
        screen.blit(smallsteps, smallsteps.get_rect(center = rect5.center))
    else:
        pygame.draw.rect(screen, ic, rect5)
        screen.blit(smallsteps, smallsteps.get_rect(center = rect5.center))
       
## Creats a button and displays it on the screen
## @param x is the x position of the rect on the screen
## @param y is the y position of the rect on the screen
## @param w is the width of the rect on the screen
## @param h is the height of the rect on the screen
## @param ic is the color on the screen before the mouse hovers
## @param ac is the color on the screen while the mouse hovers
## @param screen display surface
## @param action tell the funtion which functions to execute
def button(x, y, w, h, ic, ac, screen, action=None):
    global isDead
    global pathLen
    global visitedLen 
    global algoName

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
            isDead = False
            pathLen = 0
            visitedLen = 0
            algoName = ""
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
                algoName = "DFS"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat1", fireStartLoc)
                algoResult = sol.dfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))

                if stepPrint:       
                    for i, curr in enumerate([ele for ele in reversed(finalPath)]):
                        pathLen += 1
                        arr[curr[0]][curr[1]] = "2"
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
                        if escaped(curr) or died(curr):
                            visitedLen = len(visited)
                            break
                else:
                    mazePath(visited, finalPath)
                    board = drawBoard(MAZE_SIZE)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()
                pygame.time.delay(100)

            elif action == "bfs" and strat1:
                algoName = "BFS"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat1", fireStartLoc)
                algoResult = sol.bfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                
                if stepPrint:       
                    for i, curr in enumerate([ele for ele in reversed(finalPath)]):
                        pathLen += 1
                        arr[curr[0]][curr[1]] = "2"
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
                        if escaped(curr) or died(curr):
                            visitedLen = len(visited)
                            break
                else:
                    mazePath(visited, finalPath)
                    board = drawBoard(MAZE_SIZE)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()
                pygame.time.delay(100)

            elif action == "a*" and strat1:
                algoName = "A*"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat1", fireStartLoc)
                algoResult = sol.a_star()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))

                if stepPrint:                       
                    for i, curr in enumerate([ele for ele in reversed(finalPath)]):
                        pathLen += 1
                        arr[curr[0]][curr[1]] = "2"
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
                        if escaped(curr) or died(curr):
                            visitedLen = len(visited)
                            break
                else:
                    mazePath(visited, finalPath)
                    board = drawBoard(MAZE_SIZE)
                    screen.blit(board, board.get_rect())
                    pygame.display.update()
                pygame.time.delay(100)

            elif action == "dfs" and strat2:
                algoName = "DFS"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat2", fireStartLoc)
                algoResult = sol.dfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                    
                notComplete = True
                while notComplete:
                    pathLen += 1
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    sol = Solution(arr, pos, "strat2", fireStartLoc)
                    algoResult = sol.dfs()
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                    if escaped(pos) or died(pos):
                        visitedLen = len(visited)
                        notComplete = False
                pygame.time.delay(1000)

            elif action == "bfs" and strat2:
                algoName = "BFS"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat2", fireStartLoc)
                algoResult = sol.bfs()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                visitedLen = len(visited)
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    pathLen += 1
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    sol = Solution(arr, pos, "strat2", fireStartLoc)
                    algoResult = sol.bfs()
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                    if escaped(pos) or died(pos):
                        
                        notComplete = False
                pygame.time.delay(1000)

            elif action == "a*" and strat2:
                algoName = "A*"

                cleanGame()
                arr = readGame(GAMEFILE)
                if isfireOn:
                    arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat2", fireStartLoc)
                algoResult = sol.a_star()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                visitedLen = len(visited)
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    pathLen += 1
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    sol = Solution(arr, pos, "strat2", fireStartLoc)
                    algoResult = sol.a_star()
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                    if escaped(pos) or died(pos):
                        notComplete = False
                pygame.time.delay(1000)

            elif action == "a*" and strat3:
                algoName = "A*"
                cleanGame()
                arr = readGame(GAMEFILE)
                arr[fireStartLoc[0]][fireStartLoc[1]] = "f"
                writeGame(arr, FIREFILE)
                finalPath = {}
                sol = Solution(arr, (0, 0), "strat3", fireStartLoc)
                algoResult = sol.a_star()
                backtrack_info = algoResult[0]
                visited = algoResult[1]
                visitedLen = len(visited)
                if backtrack_info != {}:
                    finalPath = sol.create_solution(backtrack_info, (0, 0))
                notComplete = True
                while notComplete:
                    pathLen += 1
                    arr = mazeStep(visited, finalPath, screen)
                    pos = position.get_nowait()
                    sol = Solution(arr, pos, "strat3", fireStartLoc)
                    algoResult = sol.a_star()
                    backtrack_info = algoResult[0]
                    visited = algoResult[1]
                    if backtrack_info != {}:
                        finalPath = sol.create_solution(backtrack_info, pos)
                    if escaped(pos) or died(pos):
                        notComplete = False
                pygame.time.delay(1000)

## Draws text onto the display 
## @param text is the string text which gets displayed
## @param font is the pygame font 
## @param color is the color of the text
## @param screen display surface
## @param x is the x position of the text on the screen
## @param y is the y position of the text on the screen
def draw_text(text, font, color, screen, x, y):
    textobj = font.render(text, True, color)
    screen.blit(textobj, (x, y))

## Draws the name of the algorithm picked
## @param screen display surface
def draw_textAlgoName(screen):
    global algoName
    if algoName == "":
        draw_text("None", pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 250)
    else:
        draw_text(algoName, pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 250)

## Draws the status of the agent
## @param screen display surface
def draw_textStatus(screen):
    arr = readGame(GAMEFILE)
    if arr[(len(arr)-2)][(len(arr)-1)] == "2" or arr[(len(arr)-1)][(len(arr)-2)] == "2":
        draw_text('Escaped', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 275)
    elif isDead:
        draw_text('Died', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 275)
    else:
        draw_text('Alive', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 275)

## Draws the length of final path used by the agent
## @param screen display surface
def draw_textPathLen(screen):
    global pathLen
    draw_text(str(pathLen), pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 300)

## Draws the length of visited path
## @param screen display surface
def draw_textVisitedLen(screen):
    global visitedLen
    draw_text(str(visitedLen), pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 275, 325)

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

    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False

        draw_text('MAZE ON FIRE', pygame.font.SysFont("ocraextended", 50), (255, 255, 255), screen, SIZE + 20, 10)
        dice = pygame.image.load('./assets/dice2.png').convert_alpha()
        firedice = pygame.image.load('./assets/smallfiredice.png').convert_alpha()

        button(SIZE + 108, 75, 100, 50, DARKER, LIGHTDARK, screen, "clear")
        buttonImage(SIZE + 218, 75, 50, 50, DARKER, LIGHTDARK, dice, dice, screen, "rerollMAZE") #rerolls the maze and the fire.
        buttonImage(SIZE + 278, 75, 50, 50, DARKER, LIGHTDARK, firedice, firedice, screen, "rerollFIRE") #rerolls the fire.

        # fire reroll pos SIZE + 338, 75, 50, 50

        button(SIZE + 5, 195, 121, 50, DARKER, LIGHTDARK, screen, "dfs")
        button(SIZE + 5 + 121 + 10, 195, 121, 50, DARKER, LIGHTDARK, screen, "bfs")
        button(SIZE + 5 + 242 + 20, 195, 121, 50, DARKER, LIGHTDARK, screen, "a*")

        buttonToggle(DARKER, LIGHTDARK, screen)

        draw_text('Clear', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 108 + 5, 82)
        draw_text('DFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 30, 205)
        draw_text('BFS', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 30, 205)
        draw_text('A*', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 40, 205)

        draw_text('STRAT1', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 5, 145)
        draw_text('STRAT2', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 121 + 10 + 5, 145)
        draw_text('STRAT3', pygame.font.SysFont("ocraextended", 30), (255, 255, 255), screen, SIZE + 5 + 242 + 20 + 10, 145)

        draw_text('Algorithm picked     :', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 250)
        draw_textAlgoName(screen)

        draw_text('Status               :', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 275)
        draw_textStatus(screen)

        draw_text('Blocks in final path :', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 300)
        draw_textPathLen(screen)
        
        draw_text('Blocks visited       :', pygame.font.SysFont("ocraextended", 20), (255, 255, 255), screen, SIZE + 10, 325)
        draw_textVisitedLen(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()