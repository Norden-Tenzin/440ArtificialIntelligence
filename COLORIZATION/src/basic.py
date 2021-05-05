import sys, os, time, threading
import cv2
import random
import matplotlib.pyplot as plt
import numpy as np

from helper import *
from clusterInfo import *

def basic_agent(left_image, right_image):
    # get kmeans data
    # determine the best 5 representative colors.
    print("Executing K Means")
    k, pix_wit_clu = kmeans(left_image)

    # convert left image with kmeans value
    # replace the true color with the nearest representative color from the clustering.
    replacedLeft = np.copy(replaceLeft(left_image, k, pix_wit_clu))
    
    # show image
    # cv2.imshow("replacedLeft", replacedLeft)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    
    # convert left, right image to greyscale
    left_grey = convert_grey(left_image)[0]
    right_grey, right_grey_copy = convert_grey(right_image)
    # create patch from left grey_image
    leftPatches = create_patch(left_grey)
    
    # For each 3x3 grayscale pixel patch in the test data
    for row in range(1, len(right_grey) - 1):
        printProgressBar(row + 1, len(right_grey)-1, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for col in range(1, len(right_grey[row]) - 1):
            sixPatchesPos = [[0], [0], [0], [0], [0], [0]]
            sixPatchesClu = [[-1], [-1], [-1], [-1], [-1], [-1]]
            sixPatchesMin = [5000, 5000, 5000, 5000, 5000, 5000]
            
            # Find the six most similar 3x3 grayscale pixel patches in the training data
            # goes through all the left patch takes more than 1day
            patches = random.sample(list(leftPatches), 1000)
            for lPatch in patches:
                distance = get_dist(lPatch[0], right_grey[row - 1: row + 2, col - 1: col + 2])
                # compare with saved sixPatch
                index = 0
                for i in range(0, len(sixPatchesMin)):
                    if sixPatchesMin[i] > distance:
                        index = i
                        # relocate sixPatchePos and min data
                        if index != len(sixPatchesMin) - 1:
                            for j in range(len(sixPatchesMin) - 2, index - 1, -1):
                                sixPatchesMin[j+1] = sixPatchesMin[j]
                                sixPatchesPos[j+1] = sixPatchesPos[j]
                        # insert new sixpatch value
                        sixPatchesMin[index] = distance
                        sixPatchesPos[index] = lPatch[1]
                        break
            # save sixpatch's cluster number
            for i in range(0, len(sixPatchesMin)):
                sixPatchesClu[i] = pix_wit_clu[sixPatchesPos[i][0]][sixPatchesPos[i][1]].clu
            
            # For each of the six identified patches, take the color representative of the re-colored middle pixel.
            try:
                frequent = mode(sixPatchesClu)
                right_grey_copy[row][col] = k[frequent]
            except:
                tie = sixPatchesClu[random.randint(0, len(sixPatchesClu) - 1)]
                right_grey_copy[row][col] = k[tie]
    
    cv2.imshow("replacedLeft", replacedLeft)
    cv2.waitKey()
    cv2.destroyAllWindows()

    cv2.imshow("right_grey", right_grey)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
    cv2.imshow("right_grey_copy", right_grey_copy)
    cv2.waitKey()
    cv2.destroyAllWindows()
    exit()
    """
    # combine replacedLeft with right_grey_copy
    result = []

    for i in range(0, len(replacedLeft)):
        result.append(list(replacedLeft[i]) + list(right_grey_copy[i]))
    
    plt.imshow(result)
    plt.show()
    """
                    
def replaceLeft(left_image, k, pix_wit_clu):
    for row in range(0, len(left_image)):
        for col in range(0 , len(left_image[row])):
            left_image[row][col] = k[pix_wit_clu[row][col].clu]
    return left_image

def kmeans(left_image):
    k = []
    pix_wit_clu = get_clus_list(left_image)
    sum_list = []
    cnt = []

    # create 5 random pos for k
    # random between 0~255?
    for i in range(0, 5):
        row = random.randint(0, len(left_image) - 1)
        col = random.randint(0, len(left_image[0]) - 1)
        k.append(list(left_image[row][col]))
    
    # initialize list
    for i in range(0, len(k)):
        cnt.append(0)
        sum_list.append([0,0,0])

    while(True):
        animated_loading(1)
        isConvergence = True
        # Loop for all pixel
        for row in range(len(left_image)):
            for col in range(len(left_image[row])):
                temp = []

                # find nearest k for every pixel
                for i in range(len(k)):
                    temp.append(get_dist(left_image[row][col], k[i]))
                min_dist = min(temp)
                clu_index = temp.index(min_dist)

                # save a pixel data with cluster index
                pix_wit_clu[row][col].clu = clu_index
                
                # add [r,g,b] value for each cluster for cal average
                # count the number of data in each cluster
                sum_list[pix_wit_clu[row][col].clu][0] += pix_wit_clu[row][col].r
                sum_list[pix_wit_clu[row][col].clu][1] += pix_wit_clu[row][col].g
                sum_list[pix_wit_clu[row][col].clu][2] += pix_wit_clu[row][col].b
                cnt[pix_wit_clu[row][col].clu] += 1

        # calculate average of each cluster
        for i in range(0, len(k)):
            for j in range(0, 3):
                # when cnt = 0 -> error
                if cnt[i] != 0:
                    ave = int(sum_list[i][j] / cnt[i])
                else:
                    ave = 0
                # if there is big difference between average and k value, take average as a new k value (new center)
                # running this until there is no diff takes lots of time.
                if abs(ave - k[i][j]) != 0:
                    k[i][j] = ave
                    isConvergence = False

        # Run this loop untill there is only no or little bit difference
        if isConvergence:
            # return k and pixel value with their cluster index    
            return k, pix_wit_clu

def get_clus_list(image):
    result = np.empty((len(image), len(image[0])), object)

    for row in range(len(image)):
        for col in range(len(image[row])):
            result[row][col] = ClusterInfo(image[row][col][0], image[row][col][1], image[row][col][2], 0)
    return result

def get_dist(begin, end):
    result = np.linalg.norm(begin - end)
    return result

def create_patch(image):
    result = []

    for row in range(1, len(image) - 1):
        for col in range(1, len(image[row]) - 1):
            result.append((image[row - 1: row + 2, col - 1: col + 2], (row, col)))
    return result

def convert_grey(image):
    result = np.copy(image)
    copy = np.copy(image)
    for row in range(0, len(image)):
        for col in range(0, len(image[row])):
            result[row][col]= 0.21 * image[row][col][0] + 0.72 * image[row][col][1] + 0.07 * image[row][col][2]
            copy[row][col]= 0.21 * image[row][col][0] + 0.72 * image[row][col][1] + 0.07 * image[row][col][2]
    return result, copy
