import numpy as np
import cv2 as cv
import sys
import sobel

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

# magnitude should be thresholded
def hough(mag:np.ndarray,dir:np.ndarray,hough_threshold=100,min_radius=10,max_radius=100)->[[]]:
    parameter_space=np.zeros((mag.shape[0],mag.shape[1],max_radius+1))
    for i in range(0,mag.shape[0]):
        for j in range(0,mag.shape[1]):
            if mag[i,j]==255:
                # increment all points on line of possible radia
                for r in range(min_radius,max_radius+1):
                    y_c=i-int(r*np.sin(dir[i,j]))
                    x_c=j+int(r*np.cos(dir[i,j]))
                    if (y_c>=0) and (y_c<parameter_space.shape[0]) and (x_c>=0) and (x_c<parameter_space.shape[1]):
                        parameter_space[y_c,x_c,r]+=1
    # implement thresholding
    return parameter_space

# Create image to show intensity from hough space
# hough_space=[[x_c,y_c,r]]
def hough_magnitude(hough_space:np.ndarray, threshold=10):
    img=np.ndarray(hough_space.shape[0:2])
    max=-sys.maxsize; min=sys.maxsize # for normalisation
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            n=np.sum(hough_space[i,j,:]) # sum of votes for all radia
            if (n<threshold): img[i,j]=0
            else: img[i,j]=n

            if (n>max): max=n
            if (n<min): min=n

    print(min,max)
    print(hough_space.max())
    # normalise
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            img[i,j]=((img[i,j]-min)/(max-min))*255

    return img

def hough_img(colour_img:np.ndarray,hough_space:np.ndarray,threshold=5):
    overlay=np.zeros((colour_img.shape[0],colour_img.shape[1],3))
    centres=np.zeros((colour_img.shape[0],colour_img.shape[1]))

    to_plot=[]

    for i in range(0,hough_space.shape[0]):
        for j in range(0,hough_space.shape[1]):
            for k in range(0,hough_space.shape[2]):
                if (hough_space[i,j,k]>=threshold):
                    overlay[i,j]=[0,0,255]
                    to_plot.append([hough_space[i,j,k],i,j,k])
                    centres[i,j]=255
                else:
                    overlay[i,j]=colour_img[i,j]

    to_plot.sort(key=lambda x:x[0], reverse=True)
    print(len(to_plot))
    plotted=[]
    for (s,i,j,k) in to_plot:
        overlap=False

        # check whether this circle overlaps with any that have already been plotted
        for (i0,j0,k0) in plotted:
            distSq=(i0-i)**2 + (j0-j)**2
            radSumSq=(k0+k)**2

            if distSq<radSumSq:
                overlap=True
                break

        if (not overlap):
            cv.circle(overlay, (j,i), k, (0,0,255), 2)
            plotted.append([i,j,k])

    return overlay, centres

def run(path):
    img=cv.imread(path,0)
    colour_img=cv.imread(path,1)
    dx=np.matrix([[-1,0,1],[-2,0,2],[-1,0,1]])
    dy=np.matrix([[1,2,1],[0,0,0],[-1,-2,-1]])

    img_dx=sobel.convolution(img,dx)
    cv.imwrite("img/dx.png",img_dx)
    print("DX done")
    img_dy=sobel.convolution(img,dy)
    cv.imwrite("img/dy.png",img_dy)
    print("DY done")

    magnitude=sobel.magnitude(img_dx,img_dy)
    print("Magnitude done")
    magnitude=sobel.normalise(magnitude)
    cv.imwrite("img/magnitude.png",magnitude)
    print("Magnitude normalised")
    direction=sobel.direction(img_dx,img_dy)
    direction_normalised=sobel.normalise(direction,min=-np.pi,max=np.pi)
    cv.imwrite("img/direction.png",direction_normalised)
    print("Direction done")

    magnitude_threshold,direction_threshold=thresholding(magnitude,direction_normalised,threshold=150)
    print("thresholded")
    cv.imwrite("img/magnitude_threshold.png",magnitude_threshold)
    cv.imwrite("img/direction_threshold.png",direction_threshold)

    hough_space=hough(magnitude_threshold,direction,min_radius=30,max_radius=60)
    print("hough done")
    hough_image=hough_magnitude(hough_space,threshold=0)
    print("hough image")
    cv.imwrite("img/hough_img.png",hough_image)

    overlay,centres=hough_img(colour_img,hough_space,threshold=10)
    print("overlay done")
    cv.imwrite("img/centres.png",centres)
    cv.imwrite("img/overlay.png",overlay)

run("img/coins2.png")
