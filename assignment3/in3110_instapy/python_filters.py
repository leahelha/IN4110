"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np
from PIL import Image


# TASK 2    
def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image) #(H W C)
    
    # iterate through the pixels, and apply the grayscale transform   
    # Separating the image dimensions into height width and color 
    h, w, c = np.shape(image)


    for i in range(h):
        for j in range(w):
            # # Make image gray, and save in gray_image  
            gray_image[i,j] = image[i,j,0]*0.21 + image[i,j,1]*0.72 + image[i,j,2]*0.07

    
    gray_image = gray_image.astype("uint8")


    return gray_image



def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    
    sepia_image = np.empty_like(image)

    h, w, c = np.shape(image)

   
    # applying the sepia matrix
    sepia_matrix = [
                    [ 0.393, 0.769, 0.189],
                    [ 0.349, 0.686, 0.168],
                    [ 0.272, 0.534, 0.131],]



    #Iterate through the pixels
    for i in range(h):
        for j in range(w):
                 for k in range(c):
                    r, g, b = image[i, j, :]
                    sepia = r*sepia_matrix[k][0]+g*sepia_matrix[k][1]+b*sepia_matrix[k][2]
                    #print(f'i = {i}, j = {j} and k = {k}')
                    sepia_image[i,j, k] = min(255, sepia)
                    #print(sepia_image[0,0,0])
                    


    # # Return image
    
    # # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")

    return sepia_image



