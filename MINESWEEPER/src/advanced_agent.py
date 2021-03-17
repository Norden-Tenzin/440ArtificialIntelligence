import numpy as np
import random
from knowledge import *
from constants import *

class Advanced_agent():
    global change
    global found
    global Boom
    global num_random_pick
    found = 0
    Boom = 0
    change = False
    num_random_pick = 0

    def __init__(self, original_arr, copy_arr):
        # move these to knowledge later
        self.knowledge_base = list()
        self.safe_cell = list()
        self.mine_cell = list()

        self.original_arr = original_arr
        self.copy_arr = copy_arr

    def run(self):
        global change
        global num_random_pick
        # begin (select random cell)
        # print("advanced agent")
        self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))
        
        while self.chech_unclicked():
            change = False
            # remove duplicate equation
            self.knowledge_base = self.remove_duplicate(self.knowledge_base)
            # check equation to find mine or non-mine cell
            self.inference()
            # query safe cells
            self.query_all('safe')
            # query mine cells
            self.query_all('mine')
            # If there are not enought knowledge, query a random cell
            if not change:
                while self.chech_unclicked():
                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)

                    if self.copy_arr[x][y] == '?':
                        print("random pick")
                        num_random_pick += 1
                        self.query((x, y))
                        break
            # find subset in knowledge and delete subset from the superset
            if not self.mine_cell and not self.safe_cell:
                self.update_knowledge()

        print("Advanced Agent")
        print('%d x %d'%(DIM, DIM))
        print('total number of mine: %d'%(NUM_MINES))
        print('found : %d'%(found))
        print('Boom : %d'%(Boom))
        print('number of random pick : %d'%(num_random_pick))
        print('game socre: %d'%(found * (100 / NUM_MINES)))
        print(np.array(self.original_arr))
        print(np.array(self.copy_arr))
        # print(np.array(self.copy_arr))

    def update_knowledge(self):
        # print("update knowledge")
        self.knowledge_base = sorted(self.knowledge_base, key = lambda x: len(x[0]))

        for outer_data in self.knowledge_base:
            for inner_data in self.knowledge_base:
                # same data -> continue
                if outer_data == inner_data:
                    continue
                # outer is subset of inner data
                if set(outer_data[0]).issubset(set(inner_data[0])):
                    """
                    print("---------------")
                    print(self.knowledge_base)
                    print(set(inner_data[0]))
                    print(set(outer_data[0]))
                    print(list(set(inner_data[0]) - set(outer_data[0])))
                    print("---------------")
                    """
                    inner_data[0] = list(set(inner_data[0]) - set(outer_data[0]))
                    inner_data[1] = str(int(inner_data[1]) - int(outer_data[1]))
                
                if set(outer_data[0]).issuperset(set(inner_data[0])):
                    # print(set(inner_data[0]))
                    # print(set(outer_data[0]))
                    outer_data[0] = list(set(outer_data[0]) - set(inner_data[0]))
                    outer_data[1] = str(int(outer_data[1]) - int(inner_data[1]))

    def remove_duplicate(self, lst):
        temp = []

        for data in lst:
            if data not in temp:
                temp.append(data)
        # print("duplicate")
        # print(temp)
        return temp

    def inference(self):
        temp = self.knowledge_base.copy()
        
        for i in range(len(temp)):
            # print(self.knowledge_base[i][0])
            # print(self.knowledge_base[i][1])

            #print('value: %d'%(int(self.knowledge_base[i][1])))
            if len(temp[i][0]) == 0:
                # print(temp[i])
                self.knowledge_base.remove(temp[i])
                continue

            # value = 0 -> all cell are safe
            if int(temp[i][1]) == 0:
                self.knowledge_base.remove(temp[i])

                for cell in temp[i][0]:
                    self.safe_cell.append(cell)
                continue

            # value = len(cell) -> all cell are mine
            if int(temp[i][1]) == len(temp[i][0]):
                # print(self.knowledge_base)
                # print(i)
                
                self.knowledge_base.remove(temp[i])

                for cell in temp[i][0]:
                    self.mine_cell.append(cell)
        """
        print("safe list")
        print(self.safe_cell)
        print("mine list")
        print(self.mine_cell)
        """
    def query(self, pos):
        global change
        global Boom
        x = pos[0]
        y = pos[1]
        # print(self.original_arr[x][y])
        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
            # get information from cell and add equation into the knowledge
            self.add_knowledge(pos)
            # remove cell from ither equation(knowledge)
            self.remove_knowledge(pos)
            change = True
            # print(self.knowledge_base)
            # print(np.array(self.copy_arr))
        else:
            print("Boom!!")
            Boom += 1
            self.copy_arr[x][y] = self.original_arr[x][y]
            self.remove_knowledge(pos)
            # print(np.array(self.copy_arr))
            
    def remove_knowledge(self, pos):
        row = pos[0]
        col = pos[1]

        for data in self.knowledge_base:
            if (row, col) in data[0]:
                data[0].remove((row, col))

                if self.original_arr[row][col] == 'm':
                    data[1] = str(int(data[1]) - 1)

    def add_knowledge(self, pos):
        # print("add")
        row = pos[0]
        col = pos[1]
        neighb_for_equation = list()
        equation_value = self.copy_arr[row][col]
        # print(equation_value)

        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                # cell is clicked
                if self.copy_arr[i][j] ==  'F' or self.copy_arr[i][j] ==  'm':
                    # print("Flaged cell")
                    equation_value = int(equation_value) - 1
                    continue

                if self.copy_arr[i][j] !=  '?':
                    continue
                neighb_for_equation.append((i, j))
        self.knowledge_base.append([neighb_for_equation, equation_value])

    def query_all(self, status):
        
        if status == 'safe':
            while(self.safe_cell):
                safe = self.safe_cell.pop(0)
                self.query(safe)
        elif status == 'mine':
            while(self.mine_cell):
                mine = self.mine_cell.pop(0)
                self.set_flag(mine)

    def chech_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False
    
    def set_flag(self, pos):
        global change
        global found
        # print("Set flag")
        x = pos[0]
        y = pos[1]

        self.copy_arr[x][y] = 'F'
        found += 1
        change = True
        # print(self.knowledge_base)
        # remove cell from equation
        self.remove_knowledge(pos)
        # print(np.array(self.copy_arr))