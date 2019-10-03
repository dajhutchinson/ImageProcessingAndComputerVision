import cv2 as cv
import numpy as np

# Create a 256x256 black image
img=np.zeros((256,256,3),np.uint8)
img[:]=(0,0,255) # Make all pixels red

# Add white text
font = cv.FONT_HERSHEY_COMPLEX_SMALL
cv.putText(img,'HelloOpenCV!',(70,70), font, .8, (255,255,255), 1 ,cv.LINE_AA)

# Add blue line under text
cv.line(img, (74,90), (190,90), (255,0,0), 2)

# Add green smily face
cv.ellipse(img, (130,180), (25,25), 180, 180, 360, (0,255,0), 2)
cv.circle(img, (130,180), 50, (0,255,0), 2)
cv.circle(img, (110,160), 5, (0,255,0), 2)
cv.circle(img, (150,160), 5, (0,255,0), 2)

# Show image
cv.imshow("Display Window",img)
cv.waitKey(0)
cv.destroyAllWindows()
