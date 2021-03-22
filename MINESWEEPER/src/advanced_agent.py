import numpy as np
import random
from knowledge import *
from constants import *
from itertools import *

class Advanced_agent():

    def __init__(self,env, f):
        # move these to knowledge later
        self.version = "advanced"
        self.env = env
        self.original_arr = env.getAnswers()
        self.copy_arr = env.getCurr()
        self.change = False
        self.isProduct = False
        self.found = 0
        self.Boom = 0
        self.num_random_pick = 0
        self.num_uncoverd_cell = DIM * DIM
        self.prob_lst = dict()
        self.total_cell_lst = []
        self.knowledge = Knowledge()
        self.result_file = f

    def run(self):
        # begin (select random cell)
        # print("advanced agent")
        self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))

        while self.check_unclicked():
            # print(np.array(self.copy_arr))
            self.change = False
            # remove duplicate equation
            self.knowledge.knowledge_base = self.knowledge.remove_duplicate(self.knowledge.knowledge_base)
            # check equation to find mine or non-mine cell
            self.inference()
            # query safe cells
            self.query_all('safe')
            # query mine cells
            self.query_all('mine')
            # If there are not enought knowledge, query a random cell
            if not self.change:
                # ----------------------------------
                # advanced version of randim pick
                # ----------------------------------
                # self.random_probablity()
                # self.prob_lst = {}

                # ----------------------------------
                # Basic version of random pick
                # ----------------------------------
                
                while self.check_unclicked():
                    # Advanced version of random pick

                    x = random.randint(0, DIM-1)
                    y = random.randint(0, DIM-1)

                    if self.copy_arr[x][y] == '?':

                        self.num_random_pick += 1
                        self.query((x, y))
                        break
                
            # find subset in knowledge and delete subset from the superset
            if not self.knowledge.mine_cell and not self.knowledge.safe_cell:
                self.update_knowledge()
        """
        print("Advanced Agent")
        print('%d x %d'%(DIM, DIM))
        print('total number of mine: %d'%(NUM_MINES))
        print('Density : %.3f'%(NUM_MINES / (DIM * DIM)))
        print('found : %d'%(self.found))
        print('Boom : %d'%(self.Boom))
        print('number of random pick : %d'%(self.num_random_pick))
        print('game socre: %d'%(self.found * (100 / NUM_MINES)))
        #print(np.array(self.original_arr))
        print(np.array(self.copy_arr))
        """
        self.result_file.write('%d\n'%(self.found * (100 / NUM_MINES)))
        return self.found * (100 / NUM_MINES)

    def random_probablity(self):

        del self.total_cell_lst [:]
        print("random pick")
        combi_lst = list()
        self.isProduct = False
        self.num_random_pick += 1

        # cal probablity only if there are equations in the knowledge base
        if self.knowledge.knowledge_base:
            print(self.knowledge.knowledge_base)
            # get combination from each equation
            for data in self.knowledge.knowledge_base:
                combi_lst.append(list(combinations(data[0], int(data[1]))))
            # print(combi_lst)

            # get total possible scenario (duplicated)
            if len(combi_lst) != 1:
                self.isProduct = True
                # combi_lst = list(product(*combi_lst))
                combi_lst = [i for i in product(*combi_lst) if len(set(i)) == len(combi_lst)]
            print(len(combi_lst))

            # parse the data in combi_lst
            # make the list of the cell in the combi_lst with duplication (tuple list)
            for data in combi_lst.copy():
                self.parse_data(data)
            # print("---------------")
            # print(self.total_cell_lst)

            # save cnt each coord in the dictionary
            self.count_coords()
            # print(prob_lst)
            # cal probablity
            self.cal_probablity(combi_lst)

            # neighb cell (cnt number of each cell / total number of scenario)
            # reamin uncoverd cell (reamin mine / total number of uncoverd cell)
            # pick cell with min probability
            temp = min(self.prob_lst.values())
            min_prob_cell = [key for key in self.prob_lst if self.prob_lst[key] == temp]
            self.query(min_prob_cell[0])
            print(min_prob_cell[0])
      

        # If there are no equation in the knowledge base, just pick a cell randomly
        else:
            while self.check_unclicked():
                # Advanced version of random pick
                x = random.randint(0, DIM-1)
                y = random.randint(0, DIM-1)

                if self.copy_arr[x][y] == '?':
                    self.query((x, y))
                    break
                
    def parse_data(self, lst):
        temp = []

        for data in lst:
            if len(data) > 1:
                for inner_data in data:
                    temp.append(inner_data)
            else:
                temp.append((data[0][0], data[0][1]))   
        self.total_cell_lst.extend(temp)


    def cal_probablity(self, combi_lst):

        num_remain_mine = NUM_MINES - (self.found + self.Boom)

        # calculate  probablity of each cell in the knowledge base
        for data in self.prob_lst:
            # At least 2 combination with product
            if self.isProduct:
                self.prob_lst[data] = (int(self.prob_lst[data]) / len(combi_lst))
            else:
                # 1 combination without product
                self.prob_lst[data] = (int(self.prob_lst[data]) / len(combi_lst[0]))

        # calculate  probablity of each rest of uncovred cell
        if self.num_uncoverd_cell != 0:
            prob_rest_cell = num_remain_mine / (self.num_uncoverd_cell)

            for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    # uncoverd cell that is not in the knowledge basde
                    if (row, col) not in self.prob_lst and self.copy_arr[row][col] == '?':
                        self.prob_lst[(row, col)] = prob_rest_cell
        print("probablity")
        print(self.prob_lst)

    def count_coords(self):

        for data in self.total_cell_lst:
            if data in self.prob_lst:
                self.prob_lst[data] += 1
            else:
                self.prob_lst[data] = 1
    
    def update_knowledge(self):
        self.knowledge.knowledge_base = sorted(self.knowledge.knowledge_base, key = lambda x: len(x[0]))

        for outer_data in self.knowledge.knowledge_base:
            for inner_data in self.knowledge.knowledge_base:
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

    def inference(self):
        temp = self.knowledge.knowledge_base.copy()
        
        for i in range(len(temp)):
            if len(temp[i][0]) == 0:
                self.knowledge.knowledge_base.remove(temp[i])
                continue

            # value = 0 -> all cell are safe
            if int(temp[i][1]) == 0:
                self.knowledge.knowledge_base.remove(temp[i])

                for cell in temp[i][0]:
                    self.knowledge.safe_cell.append(cell)
                continue

            # value = len(cell) -> all cell are mine
            if int(temp[i][1]) == len(temp[i][0]):
                self.knowledge.knowledge_base.remove(temp[i])

                for cell in temp[i][0]:
                    self.knowledge.mine_cell.append(cell)

    def query(self, pos):

        self.num_uncoverd_cell -= 1
        x = pos[0]
        y = pos[1]

        if self.original_arr[x][y] != 'm':
            self.copy_arr[x][y] = self.original_arr[x][y]
            # get information from cell and add equation into the knowledge
            self.knowledge.add_knowledge(pos, self.copy_arr)
            # remove cell from ither equation(knowledge)
            self.knowledge.remove_knowledge(pos, self.original_arr)
            self.change = True
        else:
            # print("Boom!!")
            self.Boom += 1
            self.copy_arr[x][y] = self.original_arr[x][y]
            self.knowledge.remove_knowledge(pos, self.original_arr)

    def query_all(self, status):
        
        if status == 'safe':
            while(self.knowledge.safe_cell):
                safe = self.knowledge.safe_cell.pop(0)
                self.query(safe)
        elif status == 'mine':
            while(self.knowledge.mine_cell):
                mine = self.knowledge.mine_cell.pop(0)
                self.set_flag(mine)

    def check_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False
    
    def set_flag(self, pos):
        
        x = pos[0]
        y = pos[1]

        if self.copy_arr[x][y] != 'F':
            self.num_uncoverd_cell -= 1
            self.found += 1

        self.copy_arr[x][y] = 'F'
        self.change = True
        # remove cell from equation
        self.knowledge.remove_knowledge(pos, self.original_arr)