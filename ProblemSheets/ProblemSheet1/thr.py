import numpy as np
import cv2 as cv

img=cv.imread("mandrill.jpg",1)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

for y in range(0,gray.shape[0]):
    for x in range(0,gray.shape[1]):
        value=gray[y,x]
        if value>128:
            gray[y,x]=255
        else:
            gray[y,x]=0

# Show image
cv.imshow("Display Window",gray)
cv.waitKey(0)
cv.destroyAllWindows()
