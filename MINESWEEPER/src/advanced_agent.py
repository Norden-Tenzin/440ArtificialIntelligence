import numpy as np
import random
from knowledge import *
from constants import *
from itertools import *

class Advanced_agent():
    global change
    global found
    global Boom
    global num_random_pick
    global unique_combi_lst
    global isProduct
    global prob_lst
    global num_uncoverd_cell

    num_uncoverd_cell = DIM * DIM
    prob_lst = dict()
    isProduct = False
    unique_combi_lst = []
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
        global prob_lst
        # begin (select random cell)
        # print("advanced agent")
        self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))

        while self.check_unclicked():
            # print(np.array(self.copy_arr))
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
                # ----------------------------------
                # advanced version of randim pick
                # ----------------------------------
                self.random_probablity()
                # print(prob_lst)
                prob_lst = {}
                print(prob_lst)

                # ----------------------------------
                # Basic version of random pick
                # ----------------------------------
                """
                while self.check_unclicked():
                    # Advanced version of random pick

                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)

                    if self.copy_arr[x][y] == '?':

                        num_random_pick += 1
                        self.query((x, y))
                        break
                """
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
        #print(np.array(self.original_arr))
        #print(np.array(self.copy_arr))

    # def runStep(self):
    #         global change
    #         global num_random_pick
    #         global prob_lst
    #         # begin (select random cell)
    #         # print("advanced agent")
    #         self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))

    #         if self.check_unclicked():
    #             # print(np.array(self.copy_arr))
    #             change = False
    #             # remove duplicate equation
    #             self.knowledge_base = self.remove_duplicate(self.knowledge_base)
    #             # check equation to find mine or non-mine cell
    #             self.inference()
    #             # query safe cells
    #             self.query_all('safe')
    #             # query mine cells
    #             self.query_all('mine')
    #             # If there are not enought knowledge, query a random cell
    #             if not change:
    #                 # ----------------------------------
    #                 # advanced version of randim pick
    #                 # ----------------------------------
    #                 self.random_probablity()
    #                 # print(prob_lst)
    #                 prob_lst = {}
    #                 print(prob_lst)

    #                 # ----------------------------------
    #                 # Basic version of random pick
    #                 # ----------------------------------
    #                 """
    #                 while self.check_unclicked():
    #                     # Advanced version of random pick

    #                     x = random.randint(0, DIM-1)
    #                     y = random.randint(0, DIM-1)

    #                     if self.copy_arr[x][y] == '?':

    #                         num_random_pick += 1
    #                         self.query((x, y))
    #                         break
    #                 """
    #             # find subset in knowledge and delete subset from the superset
    #             if not self.mine_cell and not self.safe_cell:
    #                 self.update_knowledge()

    #         print("Advanced Agent")
    #         print('%d x %d'%(DIM, DIM))
    #         print('total number of mine: %d'%(NUM_MINES))
    #         print('found : %d'%(found))
    #         print('Boom : %d'%(Boom))
    #         print('number of random pick : %d'%(num_random_pick))
    #         print('game socre: %d'%(found * (100 / NUM_MINES)))
    #         #print(np.array(self.original_arr))
    #         #print(np.array(self.copy_arr))

    def random_probablity(self):
        global unique_combi_lst
        global num_random_pick
        global isProduct
        global prob_lst

        del unique_combi_lst [:]
        print("random pick")
        combi_lst = list()
        isProduct = False
        num_random_pick += 1

        # cal probablity only if there are equations in the knowledge base
        if self.knowledge_base:
            # get combination from each equation
            for data in self.knowledge_base:
                combi_lst.append(list(combinations(data[0], int(data[1]))))

            # get total possible scenario (duplicated)
            if len(combi_lst) != 1:
                isProduct = True
                combi_lst = list(product(*combi_lst))
            # remvoe duplicated result
            for data in combi_lst.copy():
                if self.is_duplicate_combination(data):
                    combi_lst.remove(data)
            
            # save cnt each coord in the dictionary
            self.count_coords()

            # cal probablity
            self.cal_probablity(combi_lst)

            # neighb cell (cnt number of each cell / total number of scenario)
            # reamin uncoverd cell (reamin mine / total number of uncoverd cell)
            # pick cell with min probability
            temp = min(prob_lst.values())
            min_prob_cell = [key for key in prob_lst if prob_lst[key] == temp]
            self.query(min_prob_cell[0])
            # print(min_prob_cell[0])

        # If there are no equation in the knowledge base, just pick a cell randomly
        else:
            while self.check_unclicked():
                # Advanced version of random pick
                x = random.randint(0, DIM-1)
                y = random.randint(0, DIM-1)

                if self.copy_arr[x][y] == '?':
                    self.query((x, y))
                    break

    def cal_probablity(self, combi_lst):
        global prob_lst
        global isProduct
        global num_uncoverd_cell
        global found
        global Boom

        num_remain_mine = NUM_MINES - (found + Boom)

        # calculate  probablity of each cell in the knowledge base
        for data in prob_lst:
            # At least 2 combination with product
            if isProduct:
                prob_lst[data] = (int(prob_lst[data]) / len(combi_lst))
            else:
                # 1 combination without product
                prob_lst[data] = (int(prob_lst[data]) / len(combi_lst[0]))

        # calculate  probablity of each rest of uncovred cell
        if num_uncoverd_cell- len(prob_lst) != 0:
            prob_rest_cell = num_remain_mine / (num_uncoverd_cell)

            for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    # uncoverd cell that is not in the knowledge basde
                    if (row, col) not in prob_lst and self.copy_arr[row][col] == '?':
                        prob_lst[(row, col)] = prob_rest_cell
        #print("probablity")
        #print(prob_lst)

    def count_coords(self):
        global unique_combi_lst
        global prob_lst

        for data in unique_combi_lst:
            if data in prob_lst:
                prob_lst[data] += 1
            else:
                prob_lst[data] = 1

    def is_duplicate_combination(self, lst):
        global unique_combi_lst
        global isProduct
        unique_temp = []
        temp = []

        for data in lst:
            if len(data) > 1:
                for inner_data in data:
                    if inner_data not in temp:
                        temp.append(inner_data)
                        unique_temp.append(inner_data)
                    else:
                        del unique_temp[:]
                        return True
            else:
                if (data[0][0], data[0][1]) not in temp:
                    unique_temp.append((data[0][0], data[0][1]))
                    temp.append((data[0][0], data[0][1]))
                else:
                    del unique_temp[:]
                    return True
            if not isProduct:
                temp = []        
        unique_combi_lst.extend(unique_temp)
        return False

    def update_knowledge(self):
        self.knowledge_base = sorted(self.knowledge_base, key = lambda x: len(x[0]))

        for outer_data in self.knowledge_base:
            for inner_data in self.knowledge_base:
                # same data -> continue
                if outer_data == inner_data:
                    continue
                # outer is subset of inner data
                if set(outer_data[0]).issubset(set(inner_data[0])):
                    inner_data[0] = list(set(inner_data[0]) - set(outer_data[0]))
                    inner_data[1] = str(int(inner_data[1]) - int(outer_data[1]))
                
                if set(outer_data[0]).issuperset(set(inner_data[0])):
                    outer_data[0] = list(set(outer_data[0]) - set(inner_data[0]))
                    outer_data[1] = str(int(outer_data[1]) - int(inner_data[1]))

    def remove_duplicate(self, lst):
        temp = []

        for data in lst:
            if data not in temp:
                temp.append(data)
        return temp

    def inference(self):
        temp = self.knowledge_base.copy()
        # (list, clue)
        for i in range(len(temp)):
            if len(temp[i][0]) == 0:
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
                self.knowledge_base.remove(temp[i])

                for cell in temp[i][0]:
                    self.mine_cell.append(cell)

    def query(self, pos):
        global change
        global Boom
        global num_uncoverd_cell

        num_uncoverd_cell -= 1
        x = pos[0]
        y = pos[1]

        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
            # get information from cell and add equation into the knowledge
            self.add_knowledge(pos)
            # remove cell from ither equation(knowledge)
            self.remove_knowledge(pos)
            change = True
        else:
            print("Boom!!")
            Boom += 1
            self.copy_arr[x][y] = self.original_arr[x][y]
            self.remove_knowledge(pos)
            
    def remove_knowledge(self, pos):
        row = pos[0]
        col = pos[1]

        for data in self.knowledge_base:
            if (row, col) in data[0]:
                data[0].remove((row, col))

                if self.original_arr[row][col] == 'm':
                    data[1] = str(int(data[1]) - 1)

    def add_knowledge(self, pos):
        row = pos[0]
        col = pos[1]
        neighb_for_equation = list()
        equation_value = self.copy_arr[row][col]

        potential_neighbor = [(row, col - 1), (row -1, col - 1), (row - 1, col), (row - 1, col + 1), (row, col + 1), (row + 1, col + 1), (row + 1, col), (row + 1, col - 1)]
        
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(self.copy_arr)) and (j >= 0 and j < len(self.copy_arr)):
                # cell is clicked
                if self.copy_arr[i][j] ==  'F' or self.copy_arr[i][j] ==  'm':
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

    def check_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False
    
    def set_flag(self, pos):
        global change
        global found
        global num_uncoverd_cell
        
        x = pos[0]
        y = pos[1]

        if self.copy_arr[x][y] != 'F':
            num_uncoverd_cell -= 1
            found += 1

        self.copy_arr[x][y] = 'F'
        change = True
        # remove cell from equation
        self.remove_knowledge(pos)