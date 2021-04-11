import sys
import os
import numpy as np

from board import *
from constants import *
from agent import *
from environment import *
import time

def main():
    if len(sys.argv) == 1:
        print('Missing Arguments')
        print('For CommandLine add argument: "-cmd"')
        print('Then specify the agent type: "agent1" or "agent2"')
        print('Example:')
        print('"python main.py -cmd agent1"')
        print('-------------------------------------------------')
        print('"python main.py -cmd test"')
        print('the test command runs both agent1 and agent2 100 times each.')
    else:
        if sys.argv[1] == "-cmd":
            if sys.argv[2] == "agent1":
                env = Environment()
                startTime = time.time()
                agent1 = Agent(env, "agent1")
                result = agent1.run()
                print("Result: " + str(result[0]+result[1]))
                print("Time Taken: " + str(time.time() - startTime))
            elif sys.argv[2] == "agent2":
                env = Environment()
                startTime = time.time()
                agent2 = Agent(env, "agent2")
                result = agent2.run()
                print("Result: " + str(result[0]+result[1]))
                print("Time Taken: " + str(time.time() - startTime))
            elif sys.argv[2] == "test":
                f = open(os.path.join(os.getcwd(), 'result.txt'), 'w')
                f1 = open(os.path.join(os.getcwd(), 'time.txt'), 'w')
                scoreAve1 = []
                scoreAve2 = []
                
                timeAve1 = []
                timeAve2 = []
                startTimeTotal = time.time()
                for i in range(2):
                    printProgressBar(i, 10, prefix = 'Progress:', suffix = 'Complete', length = 50)

                    env = Environment()
                    f.write("Basic Agent1\n")
                    f1.write("Basic Agent1\n")

                    for j in range(3):
                        startTime = time.time()
                        agent1 = Agent(env, "agent1")
                        result = agent1.run()
                        scoreAve1.append(result[0]+result[1])
                        timeAve1.append((time.time() - startTime))
                        f.write('search : %d   dist : %d    Total : %d\n'%(result[0], result[1], result[0] + result[1]))
                        f1.write('TimeTaken : %f\n'%(time.time() - startTime))
                    f.write('\n\n\n')
                    f1.write('\n\n\n')

                    f.write("Basic Agent2\n")
                    f1.write("Basic Agent2\n")
                    for j in range(3):
                        startTime = time.time()
                        agent2 = Agent(env, "agent2")
                        result = agent2.run()
                        scoreAve2.append(result[0]+result[1])
                        timeAve2.append((time.time() - startTime))
                        f.write('search : %d   dist : %d    Total : %d\n'%(result[0], result[1], result[0] + result[1]))
                        f1.write('TimeTaken : %f\n'%(time.time() - startTime))
                    printProgressBar(i + 1, 10, prefix = 'Progress:', suffix = 'Complete', length = 50)
                f.write('\n\n\n')
                f.write('basic Agent1 score ave : %.3f\n'%(np.average(scoreAve1)))
                f.write('basic Agent2 score ave : %.3f'%(np.average(scoreAve2)))
                
                f1.write('basic Agent1 time ave : %.3f\n'%(np.average(timeAve1)))
                f1.write('basic Agent2 time ave : %.3f\n'%(np.average(timeAve2)))
                f1.write('Total time: %.3f'%(time.time() - startTimeTotal))
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