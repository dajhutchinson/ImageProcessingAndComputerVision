import cv2 as cv
import numpy as np
import sys

# Load image
img=cv.imread("mandrill1.jpg",1)
new_img=np.zeros((512,512,3),np.uint8)

"""
HOW TO CORRUPT
for y in range(0,512):
    new_y=(y+32)%512
    for x in range(0,512):
        new_x=(x+32)%512
        img[y,x,2]=img[new_y,new_x,2]

"""
for x in range(511,-1,-1):
    new_x=(x+32)%512
    for y in range(511,-1,-1):
        new_y=(y+32)%512
        img[new_y,new_x,2]=img[y,x,2]

cv.imwrite("mandrill1_fix.jpg",img)
print("Image 'mandrill1_fix.jpg' created.")
