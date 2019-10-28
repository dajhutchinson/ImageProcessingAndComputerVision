import numpy as np
import cv2 as cv
import sys

def convolution(image:[[]],kernel:[[]]) -> [[]]:
    radius_x=int((kernel.shape[0]-1)/2)
    radius_y=int((kernel.shape[1]-1)/2)

    output=np.zeros(image.shape)

    padded_input=cv.copyMakeBorder(image,radius_y,radius_y,radius_x,radius_x,cv.BORDER_REPLICATE)

    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            sum=0.0
            for m in range(-radius_x,radius_x+1):
                for n in range(-radius_y,radius_y+1):
                    image_x=i+m+radius_x
                    image_y=j+n+radius_y
                    kernel_x=m+radius_x
                    kernel_y=n+radius_y

                    image_val=padded_input[image_x,image_y]
                    kernel_val=kernel[kernel_x,kernel_y]

                    sum+=image_val*kernel_val
            output[i,j]=sum
    return output

def normalise(img:[[]],min=None,max=None) -> [[]]:
    min_set=not(min is None)
    max_set=not(max is None)
    normalised=np.zeros(img.shape)
    if (not min_set): min=sys.maxsize
    if (not max_set): max=-sys.maxsize
    for i in range (0,img.shape[0]):
        for j in range (0,img.shape[1]):
            if (img[i,j]<min) and (not min_set):
                min=img[i,j]
            elif (img[i,j]>max) and (not max_set):
                max=img[i,j]

    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            normalised[i,j]=int(((img[i,j]-min)/(max-min))*255)
    return normalised

def magnitude(dx:[[]],dy:[[]]) -> [[]]:
    m=np.zeros(img.shape)

    for i in range(0,m.shape[0]):
        for j in range(0,m.shape[1]):
            m[i,j]=np.sqrt(dx[i,j]**2 + dy[i,j]**2)

    return normalise(m)

def direction(dx:[[]],dy:[[]]) -> [[]]:
    d=np.zeros(dx.shape)
    for i in range(0,dx.shape[0]):
        for j in range(0,dx.shape[1]):
            if dx[i,j]==0:
                dx[i,j]=1/sys.maxsize
            d[i,j]=np.arctan2(dy[i,j],dx[i,j])
    normalised=normalise(d,min=-np.pi,max=np.pi)
    return normalised

dx=np.matrix([[-1,0,1],[-2,0,2],[-1,0,1]])
dy=np.matrix([[1,2,1],[0,0,0],[-1,-2,-1]])

img=cv.imread("img/coins1.png",cv.IMREAD_GRAYSCALE)

# dx gradient
convolved_dx=convolution(img,dx)
normalised_dx=normalise(convolved_dx)
cv.imwrite("img/dx.png",normalised_dx)

# dy gradient
convolved_dy=convolution(img,dy)
normalised_dy=normalise(convolved_dy)
cv.imwrite("img/dy.png",normalised_dy)

# magnitude
normalised_mag=magnitude(convolved_dx,convolved_dy)
cv.imwrite("img/magnitude.png",normalised_mag)

# direction
normalised_dir=direction(convolved_dx,convolved_dy)
cv.imwrite("img/direction.png",normalised_dir)
