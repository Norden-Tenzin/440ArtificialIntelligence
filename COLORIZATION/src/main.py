from basic import *
from advanced import *

import cv2
import copy

def main():
    print("start")

    # Read image
    image = cv2.imread(r'C:\Users\sangkyun\Desktop\test1.jpg', cv2.IMREAD_UNCHANGED)

    """
    # show image
    cv2.imshow("original", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    """

    height = image.shape[0]
    width = image.shape[1]

    # cut image
    width_half = int(width / 2)
    left_image = image[:, :width_half]
    right_image = image[:, width_half:]

    # basic agent
    # basic_agent(copy.deepcopy(left_image), copy.deepcopy(right_image))

    # advanced agent
    advanced_agent(copy.deepcopy(left_image), copy.deepcopy(right_image))


if __name__ == "__main__":
    main()