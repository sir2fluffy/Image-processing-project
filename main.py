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



# for index,colour in enumerate(("red","green","blue")):
#     pl.hist(rgb_image[:,:,index].flatten(),50,color = colour)
#     pl.ylim(0,20000)
#     pl.show()

def findColours(wraped_image):
    wraped_image2 = wraped_image.copy()
    colour_array = np.zeros((4,4,3),np.uint8)
    colour_array_symbol = np.empty((4,4),np.str)
    colour_value_dict = {"r":[0,0,255],"g":[0,255,0],'b':[255,0,0],"y":[0,255,255]}#bgr
    def to_image_coords(coord):
        return coord*85 + 73
    
    square_size = 75
    
    for x in range(0,4):
        x_ = to_image_coords(x)
        for y in range(0,4):
            y_ = to_image_coords(y)
            # cv.imshow(f"square {x, y}",wraped_image[x_:x_+square_size,y_:y_+square_size,:])#shows the selected square
            # cv.waitKey(0)
            
            for colour in range(0,3): #b = 0, g = 1, r = 2
                average = int(np.average(wraped_image[x_:x_+square_size,y_:y_+square_size,colour]))
                colour_array[x,y,colour] = average# now that we have an array of the average rgb values for each square we need to 
            b, g, r = colour_array[x,y,:]
            colour_average = np.average(colour_array[x,y,:])
            if r > colour_average and b < colour_average and g < colour_average:
                colour = "r"
            elif b > colour_average and r < colour_average and g < colour_average:
                colour = "b"
            elif g > colour_average and r < colour_average and b < colour_average:
                colour = "g"
            elif g > colour_average and r > colour_average and b < colour_average:
                colour = "y"
            else:
                print(r , g , b)
                print(x, y)
                cv.imshow("ahhhhhh",wraped_image)
                cv.waitKey(0) 
                exit()
            cv.circle(wraped_image2,(y_+25,x_+25),17 ,color = [0,0,0],thickness = 10)
            cv.circle(wraped_image2,(y_+25,x_+25),15 ,color = colour_value_dict[colour],thickness = 10)
            colour_array_symbol[x,y] = colour
    cv.imshow("warp",wraped_image2)
    cv.waitKey(0)
    return colour_array_symbol
          
               
        
            
    
#findColours(rgb_image)

def find_circles(rgb_image):
    
    # cv.imshow("rgb",rgb_image)
    # cv.waitKey(0)

    threshold_value = 100
    threshold = cv.threshold(rgb_image[:,:,0], threshold_value, 255, cv.THRESH_BINARY_INV)[1]   * cv.threshold(rgb_image[:,:,1], threshold_value, 255, cv.THRESH_BINARY_INV)[1]    * cv.threshold(rgb_image[:,:,2], threshold_value, 255, cv.THRESH_BINARY_INV)[1]   


    # cv.imshow("threshold",threshold)
    # cv.waitKey(0)
    
    circles_only = (cv.medianBlur(threshold, 5)) # threshold out all of non circles objects on the image
    
    # cv.imshow("circles",circles_only)
    # cv.waitKey(0)
    
    cnts = cv.findContours(circles_only, cv.RETR_EXTERNAL,	cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    centers = np.zeros((4,2))
    
    for index, cnt in enumerate(cnts):
        # compute the center of the contour
        moment = cv.moments(cnt)
        center = (int(moment["m10"] / moment["m00"]),int(moment["m01"] / moment["m00"])) # finds coords of the centers
        centers[index,:] = center #store centers, to find centers of grid, note will not always be center of grid but is an adequate approximation, just need to find bounding corners
        	
        # draw the contour and center of the shape on the image
        #cv.drawContours(rgb_image, [cnt], -1, (0, 255, 0), 2)
        #cv.circle(rgb_image, center, 7, (255, 255, 255), -1)
    	
    	
    	# show the image
    print("centers")
    return centers

# now that we have the circles we need to contour them and find their centers
def unwarp(rgb_image):
    """requires only the circles on the image to be white and everything else to be black returns the unwraped image that has the same form as the org images"""
    centers = find_circles(rgb_image)
        
    grid_center_approx = np.array ((int(np.average(centers[:,0])), int(np.average(centers[:,1])))) # so the point with with both coords less than the center is bottom left
    
    rect = np.zeros((4,2),np.float32) #make new array to popualte with centers in order of c as iamge orgin 0,0 is top left
    

     
    if np.shape(centers) != (4 ,2):
        print("not 4 centers")
        exit()



    def bearing(point, center):
        x, y = point
        xc, yc = center
        dx = abs(x-xc)
        dy = abs(y-yc)
        
        theta = np.arctan(dy/dx)*180/np.pi
        
        if y <= yc:
            if x <= xc:
                correction = 0
            else:
                correction = -180  # correction - theta
        else:
            if x <= xc:
                correction = -360
            else:
                correction = +180
                
        return abs(theta+correction)
             
    centers_2 = np.zeros((4,3))
    centers_2[:,0:2] = centers
    for index, point in enumerate(centers):#remeber that pervious system seperated screen into 4 quadrants
        x, y = point
        xc, yc = grid_center_approx
        #see which quadrant it is in so i can see if to add 90 a bunch of times
        angle = bearing(point, grid_center_approx)
        
        # print(angle)
        
        centers_2[index,2] = angle
    centers_2 = centers_2[np.argsort(centers_2[:, 2])]
    # print(centers_2)

    #cv.circle(rgb_image, grid_center_approx, 7, (255, 0, 255), -1)
    
    
    # cv.imshow("Image", rgb_image)
    # cv.waitKey(0)
    
    #to make it more readable
    
    rect = np.zeros((4,2),np.float32)
    
    rect[:,:] = centers_2[:,0:2]
    #print(tl, tr, br, bl)
    
    
    
    #no point in enlarging so may as well make image size the maxium size of the lines that bound the grid
    
    
    
    
    #maxSize = int(max(np.linalg.norm(bl-tl),np.linalg.norm(br-tr),np.linalg.norm(bl-br),np.linalg.norm(tr-tl)))
    
    #want a square image
    
    
    dst = np.array(  [[25, 25] ,[444,  25] ,[444, 444], [ 25, 444]]    ,np.float32) #can't be 64 flaot otherwise wont work
    
    
    
    
    M = cv.getPerspectiveTransform(rect, dst)
    warp = cv.warpPerspective(rgb_image, M, (480, 480))
    return warp
 
 
    


def main():
    for file in os.listdir("images2"):
        
        
        path = f"images2\{file}"
        print(file)
        rgb_image = cv.imread(path) 
        
        warp = unwarp(rgb_image)
        
        print(findColours(warp))  
        
        # cv.imshow(file,warp)
        # cv.waitKey(0)
        print("\n"*3)
    
    #input_image = cv.imread(path,cv.IMREAD_GRAYSCALE)# make image grey, just to locate the circles -> boxes
    #smooth_image = cv.GaussianBlur(input_image, [3,3],1,1)# attempt to remove some noise

# cv.imshow("greyblur",smooth_image)
# cv.waitKey(0)


main()


# path = f"images2\proj1_1.png"
# rgb_image = cv.imread(path) 
        
# warp = unwarp(rgb_image)
# cv.imshow("warped",warp)
# cv.waitKey(0)
# print(findColours(warp))    

# print("\n"*3)

