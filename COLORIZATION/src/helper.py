import itertools
import threading
import time
import sys

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
def animated_loading(i):
    if i == 1:
        chars = "/—\|" 
        for char in chars:
            sys.stdout.write('\r'+'Processing...'+char)
            time.sleep(.5)
            sys.stdout.flush() 
            
# printProgressBar(i + 1, len(currImg), prefix = 'Progress:', suffix = 'Complete', length = 50)
