# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 00:44:35 2022

@author: charl
"""

import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as pl
import imutils # convicne fucntions, maybe axe depends on how hard contours are to figure out
for file in os.listdir("images2"):
     # print(file)
     pass
path = r"images2/proj_1.png"
rgb_image = cv.imread(path)
input_image = cv.imread(path,cv.IMREAD_GRAYSCALE)# make image grey, just to locate the circles -> boxes
smooth_image = cv.GaussianBlur(input_image, [3,3],1,1)# attempt to remove some noise

# cv.imshow("greyblur",smooth_image)
# cv.waitKey(0)

pl.hist(smooth_image.flatten(),255)



threshold = cv.threshold(smooth_image, 40, 45, cv.THRESH_BINARY) # threshold the image to get only the cicles visiavble; small amount of salt and pepper noise can be removed using a median filter

cv.imshow("threshold",threshold[1])
cv.waitKey(0)

circles_only = (cv.medianBlur(threshold[1], 5)) # this last bit normalsies to a 0 and 1 binary image

cv.imshow("circles",circles_only)
cv.waitKey(0)

# now time to actually find the cicles.


circles = cv.HoughCircles(circles_only, cv.HOUGH_GRADIENT, 1,1,param1 = 1,param2 = 18 ,minRadius=5,maxRadius=30)



circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(rgb_image,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(rgb_image,(i[0],i[1]),2,(0,0,255),3)
# cv.imshow('detected circles',rgb_image)
# cv.waitKey(0)



circle_thetas = []
for index, circle in enumerate(circles[0,:]): # cicle 0 is the main one from which the angle to all other circles are chosen
    if index != 0:
        
        # print(f"{circle[:2]} - {circles[0,0,:2]}")
        vector = circle[:2] - circles[0,0,:2]
        normal_vector = np.array((0,np.linalg.norm(vector)))
        
        theta = np.arccos(np.dot(vector,normal_vector)/(np.linalg.norm(vector)*np.linalg.norm(normal_vector)))
        
        print(theta*180/np.pi)
        
    