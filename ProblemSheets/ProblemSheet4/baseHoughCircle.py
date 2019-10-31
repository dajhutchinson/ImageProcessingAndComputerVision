import numpy as np
import cv2 as cv
import sys
import sobel
"""
NOTE
This is a stripped down of houghCircle.
The main differences are:
 - It doesn't automatically chose threshold values for magnitude or circles
 - It does not stop similar circles being plotted
"""

"""
Takes in image gradient magnitude & direction and thresholds st forall (i,j)
    if m(i,j)>T:
        m(i,j)=255 and d(i,j)=d(i,j)
    else:
        m(i,j)=0 and d(i,j)=0
"""
def thresholding(mag:np.ndarray,dir:np.ndarray,threshold=64) -> "np.ndarray,np.ndarray":
    mag_thres=np.zeros(mag.shape); dir_thres=np.zeros(dir.shape)
    for i in range(0,mag.shape[0]):
        for j in range(0,mag.shape[1]):
            if (mag[i,j]>threshold):
                mag_thres[i,j]=255
                dir_thres[i,j]=dir[i,j]
            else:
                dir_thres[i,j]=128
                mag_thres[i,j]=0
    return mag_thres,dir_thres

"""
Takes in thresholded magnitude and (thresholded) direction
"""
def hough(mag:np.ndarray,dir:np.ndarray,hough_threshold=100,min_radius=10,max_radius=100)->[[]]:
    parameter_space=np.zeros((mag.shape[0],mag.shape[1],max_radius+1))
    for i in range(0,mag.shape[0]):
        for j in range(0,mag.shape[1]): # for every pixel
            if mag[i,j]==255: # if thresholded
                # Vote for all points on line which centres could side (direction of greatest change)
                for r in range(min_radius,max_radius+1):
                    psi=dir[i,j] # Direction of greatest change

                    # One direction
                    y_c=i-int(r*np.sin(psi))
                    x_c=j+int(r*np.cos(psi))
                    if (y_c>=0) and (y_c<parameter_space.shape[0]) and (x_c>=0) and (x_c<parameter_space.shape[1]): # If if image
                        parameter_space[y_c,x_c,r]+=1

                    # Opposite direction (180)
                    y_c=i+int(r*np.sin(psi))
                    x_c=j-int(r*np.cos(psi))
                    if (y_c>=0) and (y_c<parameter_space.shape[0]) and (x_c>=0) and (x_c<parameter_space.shape[1]): # If in image
                        parameter_space[y_c,x_c,r]+=1

    # implement thresholding
    return parameter_space

"""
Creates an image to show the number of votes for each pixelsummed across all radii
Purely for visualising hough space
"""
def hough_magnitude(hough_space:np.ndarray, threshold=10):
    img=np.ndarray(hough_space.shape[0:2])
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            n=np.sum(hough_space[i,j,:]) # sum of votes for all radia
            if (n<threshold): img[i,j]=0
            else: img[i,j]=n

    return sobel.normalise(img)

"""
Identifies best circles & plots them
"""
def hough_img(colour_img:np.ndarray,hough_space:np.ndarray,threshold=5):
    centres=np.zeros((colour_img.shape[0],colour_img.shape[1])) # All centres

    for i in range(0,hough_space.shape[0]):
        for j in range(0,hough_space.shape[1]):
            for k in range(0,hough_space.shape[2]): # for every radius at every pixel
                if (hough_space[i,j,k]>=threshold): # if votes > threshold
                    cv.circle(colour_img, (j,i), k, (0,0,255), 2) # plot on image
                    centres[i,j]=255 # plot centre

    return colour_img, centres

def run(path):
    img=cv.imread(path,0) # Load image in grayscale
    colour_img=cv.imread(path,1) # load inmage in colour
    dx=np.matrix([[-1,0,1],[-2,0,2],[-1,0,1]]) # dx convolution matrix (Rate of change horizontally)
    dy=np.matrix([[1,2,1],[0,0,0],[-1,-2,-1]]) # dy convolution matrix (Rate of change vertically)

    # Calculate rate of change horizontally
    img_dx=sobel.convolution(img,dx)
    cv.imwrite("img/dx.png",img_dx)
    print("DX done")

    # Calculate rate of change vertically
    img_dy=sobel.convolution(img,dy)
    cv.imwrite("img/dy.png",img_dy)
    print("DY done")

    # Calculate image gradient magnitude
    magnitude=sobel.magnitude(img_dx,img_dy)
    magnitude=sobel.normalise(magnitude)
    cv.imwrite("img/magnitude.png",magnitude)
    print("Magnitude done")

    # Calculate image gradient direction
    direction=sobel.direction(img_dx,img_dy)
    direction_normalised=sobel.normalise(direction,min=-np.pi,max=np.pi)
    cv.imwrite("img/direction.png",direction_normalised)
    print("Direction done")

    # Threshold direction & magnitude
    magnitude_threshold,direction_threshold=thresholding(magnitude,direction_normalised,threshold=100)
    cv.imwrite("img/magnitude_threshold.png",magnitude_threshold)
    cv.imwrite("img/direction_threshold.png",direction_threshold)
    print("Thresholding done")

    # Calculate hough space
    hough_space=hough(magnitude_threshold,direction,min_radius=30,max_radius=80)
    hough_image=hough_magnitude(hough_space,threshold=0)
    cv.imwrite("img/hough_img.png",hough_image)
    print("Hough Done")

    overlay,centres=hough_img(colour_img,hough_space,threshold=10)
    cv.imwrite("img/centres.png",centres)
    cv.imwrite("img/overlay.png",overlay)
    print("Circles Found")

run(input())
