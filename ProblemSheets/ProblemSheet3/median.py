import numpy as np
import cv2 as cv

def median(arr:[int]) -> int:
    arr.sort()
    if len(arr)%2==1:
        mid=int(len(arr)/2)
        return arr[mid]
    mid=int(len(arr)/2)
    return (arr[mid]+arr[mid-1])/2

def median_transform(image,radius=1) -> [[]]:
    padded_input=cv.copyMakeBorder(image,radius,radius,radius,radius,cv.BORDER_REPLICATE)
    output=np.zeros(image.shape)

    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            neighbours=[]
            for m in range(-radius,radius+1):
                for n in range(-radius,radius+1):
                    image_x=i+m+radius
                    image_y=j+n+radius

                    neighbours.append(padded_input[image_x,image_y])

            output[i,j]=median(neighbours)
    return output

img=cv.imread("src/car2.png",cv.IMREAD_GRAYSCALE)
transformed=median_transform(img,radius=2)

cv.imwrite("src/median.png",transformed)
