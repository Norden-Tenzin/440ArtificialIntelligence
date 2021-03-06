import random
import numpy as np

def mineFieldMaker(dim, m):
    finalPath = []
    mines = m
    arr = [['0' for i in range(dim)] for j in range(dim)] 
    
    for i in range(m):
        row = random.randint(0, dim-1)
        col = random.randint(0, dim-1)
        curr = arr[row][col]
        if curr == "0" and mines != 0:
            arr[row][col] = 'm'
            mines -= 1

    for row, line in enumerate(arr):
        for col, item in enumerate(line):
            if arr[row][col] != "m":
                mineNeighbors = findMines((row, col), arr)
                arr[row][col] = str(mineNeighbors)
    return arr

def findMines(pos, arr):
    x = pos[0]
    y = pos[1]
    mines = 0

    potential_neighbor = [(x, y - 1), (x -1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]

    for (i, j) in potential_neighbor:
        if  (i >= 0 and i < len(arr)) and (j >= 0 and j < len(arr)):
            if arr[i][j] ==  "m":
                mines += 1
    return mines

def main():
    arr = mineFieldMaker(10, 20)
    print(np.array(arr))

if __name__ == "__main__":
    main()