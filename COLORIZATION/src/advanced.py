import numpy as np
import cv2

from basic import *

# input layer: 9 nodes (number of pixcel in patch)
# hidden layer: 5 nodes (like in lecture note)
# output layer: 3 nodes (r, g, b)

def advanced_agent(left_image, right_image):
    copyLeft = np.copy(left_image)
    # convert left to gray scale
    left_grey = convert_grey(left_image)[0]
    right_grey, right_grey_copy = convert_grey(right_image)
    # create patch with left grey image
    leftPatches = create_patch(left_grey)
    np.random.shuffle(leftPatches)
    # create weight
    # weights for between input and hidden 5 x 9
    w1 = np.random.rand(5, 9)
    # weights for between hidden and output 3 x 5
    w2 = np.random.rand(3, 5)
    group = []

    # divide patch into 100 groups
    for i in range(100):
        printProgressBar(i + 1, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
        begin = int(i * len(leftPatches) / 300)
        end = int(len(leftPatches) / 300 * (1 + i) - 1)
        group.append(leftPatches[begin:end])
    # train model with several samll patch group 100 times each
    for i, sub in enumerate(group):
        printProgressBar(i + 1, len(group), prefix = 'Progress:', suffix = 'Complete', length = 50)

        for k in range(0, 100):
            w1_sum = np.zeros((5, 9), dtype=float)
            w2_sum = np.zeros((3, 5), dtype=float)
            # run each patch in the subgroup
            for patch in sub:
                origin = copyLeft[patch[1]] / 255
                # re shape input as 1 x 9 matrix -> ex.[[a, b, c, d, e, f, g, h, i]]
                # each element is  grey scale pixel value from patch(3 x 3)
                input = np.array([patch[0].flatten()]) / 255
                # forward
                # 5 x 9 multi 9 x 1 -> 5 x 1 matrix hidden layer node values

                hidden = sigmoid(np.dot(w1, np.transpose(input)))

                # 3 x 5 multi 5 x 1 -> 3 x 1 matrix output layer node values
                output = sigmoid(np.dot(w2, hidden))
                # sum all new weight vlaue
                new_w2 = derivate_w2(hidden, output, origin, w2)
                new_w1 = derivate_w1(input, hidden, output, origin, w2, w1)
                w1_sum += new_w1
                w2_sum += new_w2
            # calculate average of new weight vlaue
            w1_ave = w1_sum / len(sub)
            w2_ave = w2_sum / len(sub)
            # update weight vlaue
            w1 = w1 - w1_ave
            w2 = w2 - w2_ave

    # test right grey image with trained model
    rightPatches = create_patch(right_grey)

    for i, patch in enumerate(rightPatches):
        printProgressBar(i + 1, len(rightPatches), prefix = 'Progress:', suffix = 'Complete', length = 50)
        # cal hidden 5 node value
        hidden = sigmoid(np.dot(w1, np.transpose(patch[0].flatten() / 255)))
        # cal output 3 node value
        output = sigmoid(np.dot(w2, hidden)) * 255
        right_grey_copy[patch[1]] = output

    result = combineImage(left_image, right_grey_copy)
    cv2.imwrite('advance_result.jpg', result)
    cv2.imshow("result", result)
    cv2.waitKey()
    cv2.destroyAllWindows()
    exit()

# result 5 x 9 matrix
# hidden and input
def derivate_w1(input, hidden, output, origin, w2, w1):
    # 5 x 9 mat
    formula2 = np.dot(sigmoidPrime(np.dot(w1, np.transpose(input))), input)
    # 5 x 1 mat
    formula1 = np.array([float(0),float(0),float(0),float(0),float(0)])
    # sigma part
    # run through the loop 3 times because of r g b
    for i in range(0, 3):
        formula1 += 2 * (output[i] - origin[i]) * sigmoidPrime(np.dot(w2[i], hidden)) * w2[i]
    # create 5 x 5 diagonal mat to multi with product_formula
    formula1 = np.diagflat(formula1)
    result = np.dot(formula1, formula2)

    return result

# result 3 x 5 matrix
# output and hidden
def derivate_w2(hidden, output, origin, w2):
    return np.dot(np.dot(2 * np.diagflat(output - np.transpose(np.array([origin]))), sigmoidPrime(np.dot(w2, hidden))), np.transpose(hidden))

def sigmoidPrime(input):
    return np.exp(-input) / np.square(1 + np.exp(-input))

def sigmoid(input):
    return 1 / (1 + np.exp(-input))