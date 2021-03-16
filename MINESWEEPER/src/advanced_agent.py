import numpy as np
import random
from knowledge import *
from constants import *

class Advanced_agent():
    def __init__(self, original_arr, copy_arr):
        # move these to knowledge later
        self.knowledfe_base = list()
        self.safe_cell = list()
        self.mine_cell = list()
        self.original_arr = original_arr
        self.copy_arr = copy_arr

    def run(self):
        self.query((random.randint(0, DIM-1), random.randint(0, DIM-1)))

        while self.chech_unclicked():
            self.query_safe_cell()
            

    def chech_unclicked(self):
        for row, line in enumerate(self.copy_arr):
                for col, item in enumerate(self.copy_arr):
                    if self.copy_arr[row][col] == '?':
                        return True
        return False