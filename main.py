# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 00:44:35 2022

@author: charl
"""

import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as pl

for file in os.listdir("images2"):
    print(file)


input_image = cv.imread("images2\org_1.png",cv.IMREAD_GRAYSCALE)

#cv.imshow("cat",input_image)

#cv.waitKey(0)

pl.hist(input_image.flatten(),255)

x = input_image

threshold = cv.threshold(input_image, 200, 256, cv.THRESH_BINARY_INV)
cv.imshow("threshold",threshold[1])
cv.waitKey(0)
