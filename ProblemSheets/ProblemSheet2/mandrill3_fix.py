import cv2 as cv
import sys

img=cv.imread("mandrill3.jpg",1)

# Convert to grayscale colour space & write
bgr_image=cv.cvtColor(img,cv.COLOR_HSV2BGR)
cv.imwrite("mandrill3_fix.jpg",bgr_image)
print("Image 'mandrill3_fix.jpg' created.")
