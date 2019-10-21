import numpy as np
import cv2 as cv

def convolution(image,kernel) -> [[]]:
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

img=cv.imread("src/car1.png",cv.IMREAD_GRAYSCALE)

#kernel=np.matrix([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
#kernel=np.matrix([[0,0,-1,0,0],[0,0,-1,0,0],[-1,-1,7,-1,-1],[0,0,-1,0,0],[0,0,-1,0,0]])
#kernel=np.matrix([[0,0,0,-1,0,0,0],[0,0,0,-1,0,0,0],[0,0,-1,-1,-1,0,0],[-1,-1,-1,16,-1,-1,-1],[0,0,-1,-1,-1,0,0],[0,0,0,-1,0,0,0],[0,0,0,-1,0,0,0]])

size=5
kX=cv.getGaussianKernel(size,-1)
kY=cv.getGaussianKernel(size,-1)
kernel=kX*kY.T

unnormalised=np.zeros((img.shape[0],img.shape[1]))
carBlurred=convolution(img,kernel)

# Normalise image
for c in range (0,3):

    min=0; max=255
    for i in range (0,carBlurred.shape[0]):
        for j in range (0,carBlurred.shape[1]):
            unnormalised[i,j]=float(2*img[i,j]-carBlurred[i,j])
            if unnormalised[i,j]<min:
                min=unnormalised[i,j]
            elif (unnormalised[i,j]>max):
                max=unnormalised[i,j]

    print(min,max)
    for i in range(0,carBlurred.shape[0]):
        for j in range(0,carBlurred.shape[1]):
            img[i,j]=int(((unnormalised[i,j]-min)/(max-min))*255)

cv.imwrite("src/sharp.png",img)
