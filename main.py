import numpy as np
import random
import pygame

from constants import *

def initialize():
    pygame.init()
    screen = pygame.display.set_mode((SIZE))
    return screen

def drawBoard(dim):
    cellSize = SIZE[0]/dim # asuming its a square
    board = pygame.Surface((cellSize * dim , cellSize * dim))
    board.fill((DARK))

    diff = 20/dim #border

    # 1x1
    for y in range(0, dim, 1):
        pygame.draw.rect(board, WHITE, (y*cellSize,0, cellSize, cellSize), 2)        


        # for fb in range(0, 8, 2):
        #     pygame.draw.rect(board, WHITE, (y*CELLSIZE, fb *
        #                                     CELLSIZE, CELLSIZE, CELLSIZE))
        # for fw in range(1, 9, 2):
        #     pygame.draw.rect(board, WHITE, ((y+1)*CELLSIZE,
        #                                     fw*CELLSIZE, CELLSIZE, CELLSIZE))

    return board

def main():
    screen = initialize()
    arr = mazeMaker(10, 0.3)
    board = drawBoard(10)
    screen.blit(board, board.get_rect())
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