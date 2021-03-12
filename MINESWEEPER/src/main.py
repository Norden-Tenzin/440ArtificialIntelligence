from basic_agent import *
from environment import *
from constants import *
import numpy as np

def main():
    env = Environment(DIM, NUM_MINE)
    # original arr
    original_arr = env.mineFieldMaker(original = True)
    # arr with '?' for agent
    copy_arr = env.mineFieldMaker(original = False)
    print(np.array(original_arr))
    # call basic agent
    agent = basic_agent(original_arr, copy_arr)
    # solving arr with basic agent
    agent.run()
    print("~~~~~~~~~end~~~~~~~~~~~~~~~~~")
    print(np.array(original_arr))

if __name__ == "__main__":
    main()