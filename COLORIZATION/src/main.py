import sys, os, time, threading
import cv2
import matplotlib.pyplot as plt
import copy

from basic import *
from advanced import *
from constants import *

def main():
    if len(sys.argv) == 1:
        print('Missing Arguments')
        print('For CommandLine add argument: "-cmd"')
        print('Then specify the type: "basic" or "advanced"')
        print('Example:')
        print('"python main.py -cmd basic"')
        print('-------------------------------------------------')
    else:
        if sys.argv[1] == "-cmd":
            # Read image
            image = cv2.imread(r""+RESIZE_BEACH1_PATH, cv2.IMREAD_UNCHANGED)
            # print("start")
            height = image.shape[0]
            width = image.shape[1]

            # cut image
            width_half = int(width / 2)
            left_image = image[:, :width_half]
            right_image = image[:, width_half:]

            if sys.argv[2] == "basic":
                print("BASIC COLORING AGENT")
                # basic agent
                basic_agent(copy.deepcopy(left_image), copy.deepcopy(right_image))
            if sys.argv[2] == "advanced":
                print("ADVANCED COLORING AGENT")
                # advanced agent
                advanced_agent(copy.deepcopy(left_image), copy.deepcopy(right_image))

if __name__ == "__main__":
    main()