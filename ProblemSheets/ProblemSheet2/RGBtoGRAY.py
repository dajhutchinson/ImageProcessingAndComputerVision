import cv2 as cv
import sys

if (len(sys.argv)!=2):
    print("No image given!")
    exit()

img_name=sys.argv[1]
img=cv.imread(img_name,1)

# End if no image loaded
if (not img.data):
    print("No image data!")
    exit()

# Convert to grayscale colour space & write
gray_image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imwrite("gray.jpg",gray_image)
print("Image 'gray.jpg' created.")
