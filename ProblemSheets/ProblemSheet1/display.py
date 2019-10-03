import numpy as np
import cv2 as cv

img=cv.imread("myimage.jpg",cv.IMREAD_UNCHANGED)

# Show image
cv.imshow("Display Window",img)
cv.waitKey(0)
cv.destroyAllWindows()
