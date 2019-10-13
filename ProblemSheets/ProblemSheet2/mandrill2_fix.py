import cv2 as cv
import numpy as np
import sys

# Load image
img=cv.imread("mandrill2.jpg",1)
new_img=np.zeros((512,512,3),np.uint8)

for y in range(0,512):
    for x in range(0,512):
        img[y,x,0]=255-img[y,x,0]
        img[y,x,1]=255-img[y,x,1]
        img[y,x,2]=255-img[y,x,2]

cv.imwrite("mandrill2_fix.jpg",img)
print("Image 'mandrill2_fix.jpg' created.")
