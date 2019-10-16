import cv2 as cv
import numpy as np

# Load image
img=cv.imread("raffles_gray.jpg",0)
box_blur=np.ones((3,3),np.float32)/9
edge_detection_0=np.matrix([[1,0,-1],[0,0,0],[-1,0,1]])
edge_detection_1=np.matrix([[0,1,0],[1,-4,1],[0,1,0]])
edge_detection_2=np.matrix([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])

def convolution(image,kernel) -> [[]]:
    # Check kernel is of valid dimensions
    if (kernel.shape[0]%2!=1) or (kernel.shape[1]%2!=1):
        print("Kernel must have odd height & width (not necessarily equal)")
        return -1

    # Create matrix for new image to be written into
    new_img=np.zeros((image.shape[0],image.shape[1],3),np.uint8)

    # number of pixels on each side of target
    min_dim_x=int((kernel.shape[1]-1)/2)
    min_dim_y=int((kernel.shape[0]-1)/2)

    # Run throug ever pixel
    for y in range(0,image.shape[0]):
        for x in range(0,image.shape[1]):

            # find left & topmost edges of pixels to check around target
            min_x=x-min_dim_x
            min_y=y-min_dim_y

            # Find pixels to use around target
            pixel_surround=np.zeros(kernel.shape)
            for i in range(min_x,min_x+kernel.shape[1]):
                for j in range(min_y,min_y+kernel.shape[0]):
                    # Only add if in range (else value will be zero & thus not affect convolution)
                    if (i>=0) and (i<=image.shape[1]-1) and (j>=0) and (j<=image.shape[0]-1):
                        pixel_surround[j-min_y,i-min_x]=img[j,i]

            # Perform convolution sum
            new_value=0
            for m in range(0,kernel.shape[0]):
                for n in range(0,kernel.shape[1]):
                    new_value+=pixel_surround[m,n]*kernel[m,n]
            new_img[y,x]=int(new_value)
        print("{}/{}".format(y,image.shape[0]))

    return new_img

convolutioned_img=convolution(img,edge_detection_0)
cv.imwrite("raffles_edge_0.jpg",convolutioned_img)
print("Image 'convolution_0.jpg' created.")

convolutioned_img=convolution(img,edge_detection_1)
cv.imwrite("raffles_edge_1.jpg",convolutioned_img)
print("Image 'convolution_1.jpg' created.")

convolutioned_img=convolution(img,edge_detection_2)
cv.imwrite("raffles_edge_2.jpg",convolutioned_img)
print("Image 'convolution_2.jpg' created.")
