"""numba-optimized filters"""
from __future__ import annotations

import numpy as np
from numba import jit
from PIL import Image

@jit 
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    
    # iterate through the pixels, and apply the grayscale transform
    h, w, c = np.shape(image)

    for i in range(h):
        for j in range(w):
            # Make image gray, and save in gray_image
            gray_image[i,j] = image[i,j,0]*0.21 + image[i,j,1]*0.72 + image[i,j,2]*0.07

    
    gray_image = gray_image.astype("uint8")

    # *** DELETE LATER
    image = Image.fromarray(gray_image)
    image.save("rain_grayscale.jpg")

    return gray_image

# *** DELETE LATER
im = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
# resized = im.resize((im.width // 2, im.height // 2))
pixels = np.asarray(im)

run = numba_color2gray(pixels)

def numba_color2sepia(image: np.array) -> np.array:
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


...
