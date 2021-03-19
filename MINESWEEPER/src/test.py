from environment import *
from maze import *
from cell import *

from constants import *
from knowledge import *
import numpy as np
import math
# en = Maze(DIM, NUM_MINES)
# print(np.array(en.shown))
# print(np.array(en.hidden))

# cell = Cell("s")
# print(cell.state)

# know = Knowledge()
# print(np.array(know.arr))

def is_duplicate_combination(lst):
        temp = list()

        for data in lst:
            print('len : %d'%(len(data)))
            print(data)
            if len(data) > 2:
                for inner_data in data:
                    if inner_data not in temp:
                        print(inner_data)
                        temp.append(inner_data)
                    else:
                        return True
            else:
                if data not in temp:
                    continue
                    #print(data)
                    #temp.append(data)
                else:
                    return True
        # print("$$$$$$$temp$$$$$$$$")
        # print(temp)
        return False

def main():
    arr = [((0, 3), (3, 0), (0, 0))]
    print(is_duplicate_combination(arr))

if __name__ == "__main__":
    main()