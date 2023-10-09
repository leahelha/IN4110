"""Cython implementation of filter functions"""
from __future__ import annotations

import cython as C

# from cython_filters import cython_color2gray, cython_color2sepia  # Import the declarations

import numpy as np # noqa



if not C.compiled:
    raise ImportError(
        "Cython module not compiled! Check setup.py and make sure this package has been installed, not just imported in-place, e.g. `pip install --editable .`."
    )


from cython.cimports.libc.stdint import uint8_t  # noqa

# we may need a 'const uint8_t' type to make sure we accept 'read-only' arrays
const_uint8_t = C.typedef("const uint8_t")

float64_t = C.typedef(C.double)


def cython_color2gray(image: C.npy_uint8[:,:,:])->C.npy_uint8[:,:,:]:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image_arr
    """

    h: C.int = image.shape[0]
    w: C.int = image.shape[1]
    c: C.int = image.shape[2]

    gray_image: C.double[:,:,:] = np.zeros((h,w,c))


    for i in range(h):
        for j in range(w):
            r: C.double = image[i, j, 0]
            g: C.double = image[i, j, 1]
            b: C.double = image[i, j, 2]
            gray: C.double = 0.21*r+0.72*g+0.07*b
            gray_image[i, j, :] = gray


    gray_image_arr: C.npy_uint8[:,:,:] = np.array(gray_image).astype("uint8")
  

    return gray_image_arr




def cython_color2sepia(image: C.npy_uint8[:,:,:])->C.npy_uint8[:,:,:]:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image_arr
    """
    
    h: C.int = np.shape(image)[0]
    w: C.int = np.shape(image)[1]
    c: C.int = np.shape(image)[2]

    sepia_image: C.double[:,:,:] = np.zeros((h,w,c))
   
    # applying the sepia matrix
    sepia_matrix = [[ 0.393, 0.769, 0.189],[ 0.349, 0.686, 0.168],[ 0.272, 0.534, 0.131]]

    


    #Iterate through the pixels
    for i in range(h):
        for j in range(w):
            for k in range(c):
                r: C.double = image[i, j, 0]
                g: C.double = image[i, j, 1]
                b: C.double = image[i, j, 2]

                sepia =  image[i, j, 0] * sepia_matrix[k][0] + image[i, j, 1] * sepia_matrix[k][1] + image[i, j, 2] * sepia_matrix[k][2]#r*sepia_matrix[k, 0]+ g*sepia_matrix[k, 1]+ b*sepia_matrix[k, 2]
                sepia_image[i, j, k] = min(255, sepia)

    # # Return image
    
    # # don't forget to make sure it's the right type!
    sepia_image_arr: C.npy_uint8[:,:,:] = np.array(sepia_image).astype("uint8")

    return sepia_image_arr
