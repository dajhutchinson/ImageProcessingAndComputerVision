import cv2 as cv
import numpy as np

# Creates a 256x256 black image
img=np.zeros((256,256,3), np.uint8)

# Add white text
font = cv.FONT_HERSHEY_COMPLEX_SMALL
cv.putText(img,'HelloOpenCV!',(70,70), font, .8, (255,255,255), 1 ,cv.LINE_AA)

# Save Unage
cv.imwrite("myimage.jpg",img)

# Show image
cv.imshow("Display Window",img)
cv.waitKey(0)
cv.destroyAllWindows()
