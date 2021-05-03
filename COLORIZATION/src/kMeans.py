import math
import csv
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import os
from PIL import Image
from constants import *
from helper import *

class kMeans():
    pass
    def __init__(self, data, k = 5, tolerance = 0.0001, iteration = 1):
        self.k = k
        self.tolerance = tolerance 
        self.iteration = iteration
        
    def run(self, data):
        flatImg = np.array(data.reshape(-1, 3))
        lower = flatImg.min(axis=0)
        upper = flatImg.max(axis=0)
        c = np.random.randint(min(lower), max(upper), size=(self.k, 3))
        cMap = np.zeros((len(data), len(data[0])))
        
        for iter_i in range(self.iteration):
            # printProgressBar(iter_i + 1, self.iteration, prefix = 'Progress:', suffix = 'Complete', length = 50)
            for i, pixels in enumerate(currImg):
                printProgressBar(i + 1, len(currImg), prefix = 'Progress:', suffix = 'Complete', length = 50)
                for j, pixel in enumerate(pixels):
                    edList = []
                    for centroid in c:
                        ed = self.euclideanDistance(pixel, centroid)
                        edList.append(ed)
                    cMap[i][j] = edList.index(min(edList))
            print(cMap[0])
            
            with open('employee_file.csv', mode='w') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                employee_writer.writerow(['John Smith', 'Accounting', 'November'])
                employee_writer.writerow(['Erica Meyers', 'IT', 'March'])
            plt.plot(cMap)
            plt.show()

    def euclideanDistance(self, x1, x2):
        squared_distance = 0
        #Assuming correct input to the function where the lengths of two features are the same
        for i in range(len(x1)):
            squared_distance += (x1[i] - x2[i])**2
        ed = math.sqrt(squared_distance)
        return ed;
    
currImg = plt.imread(RESIZE_BEACH1_PATH)
flatImg = np.array(currImg.reshape(-1, 3))

means = kMeans(5)
means.run(currImg)
# print(means.euclideanDistance([20,10,100], [100,29,200]))


def kMeans():
    k = 5
    

    print(c)
    for i, pixels in enumerate(currImg):
        for j, pixel in enumerate(pixels):
            print(pixel)
    # for kmeans_i in range(5):
    #     print('iteration: %d' % (kmeans_i))
    #     assignments = []
    #     # * update cluster assignment
    #     for i in range(len(flatImg)):
    #         idx = np.argmin(np.linalg.norm(flatImg[i] - c, axis=1))
    #         assignments.append(idx)
    #     assignments = np.array(assignments)
    #     # * update centroids based on assignment
    #     for i in range(k):
    #         centroids[i] = np.mean(data[assignments==i], axis=0)
    #         # if some centroids have no assignments, reinitialize it
    #         if (assignments==i).sum() == 0:
    #             centroids[i] = np.random.uniform(low=lower, high=upper)
    #     # * check for convergence
    #     print('centroids move by: %f' % (np.linalg.norm(centroids - prev_centroids, axis=1).max()))
    #     if prev_assignments is not None:
    #         print('assignment differs by: %d' % (np.sum((assignments - prev_assignments)!=0)))
    #     if prev_assignments is not None and np.linalg.norm(assignments - prev_assignments) == 0.:
    #         break
        
    #     prev_assignments = assignments
    #     prev_centroids = np.array(centroids)

    #     # plot the points (for toy problem)
    #     if vis:
    #         plt.figure()
    #         plt.scatter(data[assignments==0][:,0],data[assignments==0][:,1], c='r')
    #         plt.scatter(data[assignments==1][:,0],data[assignments==1][:,1], c='g')
    #         plt.scatter(data[assignments==2][:,0],data[assignments==2][:,1], c='b')

    #         plt.scatter(centroids[:,0], centroids[:,1], c=['r','g','b'])
    #         plt.show()
    
    # return centroids, assignments
