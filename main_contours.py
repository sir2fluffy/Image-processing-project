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
     # print(file)
     pass
path = "images2\org_1.png"
rgb_image = cv.imread(path)
input_image = cv.imread(path,cv.IMREAD_GRAYSCALE)# make image grey, just to locate the circles -> boxes
smooth_image = cv.GaussianBlur(input_image, [3,3],1,1)# attempt to remove some noise

# cv.imshow("greyblur",smooth_image)
# cv.waitKey(0)

for index,colour in enumerate(("red","green","blue")):
    pl.hist(rgb_image[:,:,index].flatten(),50,color = colour)
    pl.ylim(0,20000)
    pl.show()



threshold = cv.threshold(smooth_image, 220, 255, cv.THRESH_BINARY_INV) # threshold the image to get only the cicles visiavble; small amount of salt and pepper noise can be removed using a median filter

# cv.imshow("threshold",threshold[1])
# cv.waitKey(0)

shapes_only = cv.medianBlur(threshold[1], 5)

# cv.imshow("shapes",shapes_only)
# cv.waitKey(0)

contours,_=cv.findContours(shapes_only, cv.RETR_TREE,
                            cv.CHAIN_APPROX_SIMPLE)
   
# Searching through every region selected to 
# find the required polygon.
for cnt in contours :
    area = cv.contourArea(cnt)
   
    # Shortlisting the regions based on there area.
    
    approx = cv.approxPolyDP(cnt, 
                              0.009 * cv.arcLength(cnt, True), True)
   
    # Checking if the no. of sides of the selected region is 7.
    if len(approx) < 8:
        print("->",approx)
        #cv.drawContours(rgb_image, [approx], 0, (0, 0, 255), 2)
        cv.circle(rgb_image,(approx),i[2],(0,255,0),2)
# Showing the image along with outlined arrow.
cv.imshow('image2', rgb_image) 
   
# Exiting the window if 'q' is pressed on the keyboard.
if cv.waitKey(0) & 0xFF == ord('q'): 
    cv.destroyAllWindows()