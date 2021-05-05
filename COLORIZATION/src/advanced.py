import numpy as np
import cv2

from basic import *

# input layer: 9 nodes (number of pixcel in patch)
# hidden layer: 5 nodes (like in lecture note)
# output layer: 3 nodes (r, g, b)
def advanced_agent(left_image, right_image):
    print("advanced agent")
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
    num = 200
    for i in range(num):
        begin = int(i * len(leftPatches) / num)
        end = int(len(leftPatches) / num*(1 + i) - 1)
        group.append(leftPatches[begin:end])
    
    for sub in group:         
        for k in range(0, 100):
            w1_sum = np.zeros((5, 9), dtype=float)
            w2_sum = np.zeros((3, 5), dtype=float)
            for patch in sub:
                new_w2, new_w1 = training(patch[0], copyLeft[patch[1]],w1, w2)
                w1_sum += new_w1
                w2_sum += new_w2
            
            w1_ave = w1_sum / len(sub)
            w2_ave = w2_sum / len(sub)
            w1 = w1 - w1_ave
            w2 = w2 - w2_ave

    # test right grey image
    rightPatches = create_patch(right_grey)

    for patch in rightPatches:
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

def training(input, origin,w1, w2):
    origin = origin / 255
    # re shape input as 1 x 9 matrix -> ex.[[a, b, c, d, e, f, g, h, i]]
    # each element is  grey scale pixel value from patch(3 x 3)
    input = np.array([input.flatten()]) / 255

    # forward
    # 5 x 9 multi 9 x 1 -> 5 x 1 matrix hidden layer node values
    hidden = sigmoid(np.dot(w1, np.transpose(input)))
    # 3 x 5 multi 5 x 1 -> 3 x 1 matrix output layer node values
    output = sigmoid(np.dot(w2, hidden))
    # update weight vlaue
    new_w2 = derivate_w2(hidden, output, origin, w2)
    new_w1 = derivate_w1(input, hidden, output, origin, w2, w1)

    return new_w2, new_w1

# result 5 x 9 matrix
# hidden and input
def derivate_w1(input, hidden, output, origin, w2, w1):
    fornula2 = sigmoidPrime(np.dot(w1, np.transpose(input)))
    # 5 x 9 mat
    product_formula = np.dot(fornula2, input)
    # 5 x 1 mat
    sum = np.array([float(0),float(0),float(0),float(0),float(0)])

    # sigma part
    for i in range(0, 3):
        sum += (2 * (output[i] - origin[i]) * sigmoidPrime(np.dot(w2[i], hidden))) * w2[i]
    # create 5 x 5 diagonal mat to multi with product_formula
    sum = np.diagflat(sum)
    result = np.dot(sum, product_formula)

    return result

# result 3 x 5 matrix
# output and hidden
def derivate_w2(hidden, output, origin, w2):
    derivated_w2 = np.dot(2 * np.diagflat(output - np.transpose(np.array([origin]))), sigmoidPrime(np.dot(w2, hidden)))
    result = np.dot(derivated_w2, np.transpose(hidden))

    return result

def sigmoidPrime(input):
    return np.exp(-input) / np.square(1 + np.exp(-input))

def sigmoid(input):
    return 1 / (1 + np.exp(-input))