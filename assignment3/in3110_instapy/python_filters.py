"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np
from PIL import Image

import in3110_instapy
#from in3110_instapy.io import write_image #, random_image, display, read_image

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
    w, h, c = np.shape(image)

    for i in range(w):
        for j in range(h):
            #for k in range(c):
            # Separate RGB values from image
            r, g, b = image[i, j, :]

            # Make image gray, and save in gray_image
            gray = 0.21*r + 0.72*g + 0.07*b
            
            gray_image[i,j, :] = gray

    
    grayscale_array = gray_image.astype("uint8")

    
    image = Image.fromarray(grayscale_array)
    image.save("rain_grayscale.jpg")

    return grayscale_array


im = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
resized = im.resize((im.width // 2, im.height // 2))
pixels = np.asarray(resized)

run = python_color2gray(pixels)

def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    ...

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
