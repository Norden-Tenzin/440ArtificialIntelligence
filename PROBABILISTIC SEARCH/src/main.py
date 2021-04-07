import numpy as np
import os

from board import *
from constants import *
from agent import *

def main():

    f = open(os.path.join(os.getcwd(), 'result.txt'), 'w')
    scoreAve1 = []
    scoreAve2 = []

    for i in range(10):
        game = Board()
        f.write("Basic Agent1\n")

        for j in range(10):
            agent1 = Agent(game, "agent1")
            result = agent1.run()
            scoreAve1.append(result[0]+result[1])
            f.write('search : %d   dist : %d    Total : %d\n'%(result[0], result[1], result[0] + result[1]))

        f.write('\n\n\n')
        f.write("Basic Agent2\n")

        for j in range(10):
            agent2 = Agent(game, "agent2")
            result = agent2.run()
            scoreAve2.append(result[0]+result[1])
            f.write('search : %d   dist : %d    Total : %d\n'%(result[0], result[1], result[0] + result[1]))
            
    f.write('\n\n\n')
    f.write('basic Agent1 score ave : %.3f\n'%(np.average(scoreAve1)))
    f.write('basic Agent2 score ave : %.3f'%(np.average(scoreAve2)))
    print("END")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == "__main__":
    main()