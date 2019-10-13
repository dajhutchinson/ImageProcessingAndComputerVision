import cv2 as cv
import sys

# Load image
img=cv.imread("mandrill0.jpg",1)

for y in range(0,img.shape[0]):
    for x in range(0,img.shape[1]):
        bgr=img[y,x].copy()
        #print("BGR [{},{},{}]\n".format(bgr[0],bgr[1],bgr[2]))
        img[y,x,0]=bgr[2] # Red to Blue
        img[y,x,1]=bgr[0] # Blue to Green
        img[y,x,2]=bgr[1] # Green to Red
        #print("IMG [{},{},{}]\n".format(img[y,x,0],img[y,x,1],img[y,x,2]))

cv.imwrite("mandrill0_fix.jpg",img)
print("Image 'mandrill0_fix.jpg' created.")
