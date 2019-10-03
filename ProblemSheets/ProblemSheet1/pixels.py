import cv2 as cv
import numpy as np

# Creates a 256x256 black image
img=np.zeros((256,256,3), np.uint8)

for y in range(0,img.shape[0]):
    for x in range(0,img.shape[1]):
        img[y,x,0]=x
        img[y,x,1]=y
        img[y,x,2]=255-img[y,x,1]

# Show image
cv.imshow("Display Window",img)
cv.waitKey(0)
cv.destroyAllWindows()
