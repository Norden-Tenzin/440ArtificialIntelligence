import numpy as np
import random
import pygame

from constants import *

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    return screen

def drawBoard(dim):
    top = 5
    left = 5 # left = lr/2 

    # diff is the border width 
    diff = 2
    diffn = dim-1
    difft = diff * diffn
    cellSize = int((SIZE-left-difft)/dim)

    board = pygame.Surface((SIZE, SIZE))
    board.fill((DARK))
    
    # 1x1
    for row in range(0, dim, 1):
        for col in range(0, dim, 1):
            pygame.draw.rect(board, WHITE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))        


        # for fb in range(0, 8, 2):
        #     pygame.draw.rect(board, WHITE, (y*CELLSIZE, fb *
        #                                     CELLSIZE, CELLSIZE, CELLSIZE))
        # for fw in range(1, 9, 2):
        #     pygame.draw.rect(board, WHITE, ((y+1)*CELLSIZE,
        #                                     fw*CELLSIZE, CELLSIZE, CELLSIZE))

    return board

def draw(dim, cord, blockType):
    board = pygame.Surface((SIZE, SIZE))
    if(blockType == "agent"):
        pygame.draw.rect(board, WHITE, (col*cellSize + (col+1)*diff + left, top + row*diff + row*cellSize , cellSize, cellSize))        

    if(blockType == "block"):
    if(blockType == "fire"):

    # player, block and fire 
    #cord is a tuple
    #example cord 0,1 

    return board

def main():
    screen = initialize()
    arr = mazeMaker(10, 0.3)
    board = drawBoard(10)
    screen.blit(board, board.get_rect())

    changes = draw(10, (1,1), "block")
    screen.blit(changes, changes.get_rect())
    on = True
    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
        pygame.display.flip()



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
                    row[i] = "X"
                    count += 1
    
    # print(count)
    # print(np.matrix(arr))
    return arr
    
if __name__ == "__main__":
    main()