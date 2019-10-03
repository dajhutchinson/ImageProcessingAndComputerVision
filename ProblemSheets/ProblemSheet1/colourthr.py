import numpy as np
import cv2 as cv

img=cv.imread("mandrillRGB.jpg",1)

for y in range(0,img.shape[0]):
    for x in range(0,img.shape[1]):
        bgr=img[y,x]
        if bgr[0]>128:
            img[y,x,0]=255
        else:
            img[y,x,0]=0

        if bgr[1]>128:
            img[y,x,1]=255
        else:
            img[y,x,1]=0

        if bgr[2]>128:
            img[y,x,2]=255
        else:
            img[y,x,2]=0

# Show image
cv.imshow("Display Window",img)
cv.waitKey(0)
cv.destroyAllWindows()
