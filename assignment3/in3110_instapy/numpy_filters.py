"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np
from PIL import Image


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)
    h, w, c = np.shape(image)
    # Converting the original image to grayscale
    for i in range(h):
        for j in range(w):
            for k in range(c):
                gray = np.dot(image[i,j,:],[0.21, 0.72, 0.07])
                gray_image[i,j,k] = gray
                
    
    # Hint: use numpy slicing in order to have fast vectorized code
    
    # Return image (make sure it's the right type!)
    gray_image = gray_image.astype("uint8")

    return gray_image



def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")


    sepia_image = np.empty_like(image)
    h, w, c = np.shape(image)

    
    # define sepia matrix (optional: with stepless sepia changes)
    sepia_matrix =  np.array([
                    [ 0.393+(1-0.393)*(1-k), 0.769-(0.769)*(1-k), 0.1890-((0.1890)*(1-k))],
                    [ 0.349-((0.349)*(1-k)), 0.686+(1-0.686)*(1-k), 0.168-(0.168*(1-k))],
                    [ 0.272-(0.272*(1-k)), 0.534-(0.534*(1-k)), 0.131+(1-0.131)*(1-k)],])


    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix

    # Apply the matrix filter
    for i in range(h):
        for j in range(w):
            for g in range(c):
                sepia = np.dot(image[i,j,:],sepia_matrix[g])
                sepia_image[i,j,g] = min(255, sepia)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255


    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")

    return sepia_image


