from cell import *
from constants import *

class Knowledge():
    def __init__(self):
        self.arr = [[Cell("?") for i in range(DIM)] for j in range(DIM)]
        self.knowledge_base = list()
        self.safe_cell = list()
        self.mine_cell = list()

    def remove_duplicate(self, lst):
        temp = []

        for data in lst:
            if data not in temp:
                temp.append(data)
        return temp

    def remove_knowledge(self, pos, original_arr):
        row = pos[0]
        col = pos[1]

        for data in self.knowledge_base:
            if (row, col) in data[0]:
                data[0].remove((row, col))

                if original_arr[row][col] == 'm':
                    data[1] = str(int(data[1]) - 1)

    def add_knowledge(self, pos, copy_arr):
        row = pos[0]
        col = pos[1]
        neighb_for_equation = list()
        equation_value = copy_arr[row][col]

        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(copy_arr)) and (j >= 0 and j < len(copy_arr)):
                # cell is clicked
                if copy_arr[i][j] ==  'F' or copy_arr[i][j] ==  'm':
                    equation_value = int(equation_value) - 1
                    continue

                if copy_arr[i][j] !=  '?':
                    continue
                neighb_for_equation.append((i, j))
        self.knowledge_base.append([neighb_for_equation, equation_value])