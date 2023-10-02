"""Cython implementation of filter functions"""
from __future__ import annotations

import cython as C
import numpy as np
from PIL import Image

if not C.compiled:
    raise ImportError(
        "Cython module not compiled! Check setup.py and make sure this package has been installed, not just imported in-place, e.g. `pip install --editable .`."
    )

from cython.cimports.libc.stdint import uint8_t  # noqa

# we may need a 'const uint8_t' type to make sure we accept 'read-only' arrays
const_uint8_t = C.typedef("const uint8_t")
float64_t = C.typedef(C.double)


def cython_color2gray(image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    # cdef int h = image.shape[0]
    # cdef int w = image.shape[1]
    # cdef np.ndarray[np.uint8_t[:, :, :], ndim=3] gray_image
    # cdef double r, g, b

    h: C.int = image.shape[0]  #ikke definer her i .py fil
    w: C.int = image.shape[1]


    gray_image = np.empty_like(image)

    
    for i in range(h):
        for j in range(w):
            r: C.double = image[i, j, 0]
            g: C.double = image[i, j, 1]
            b: C.double = image[i, j, 2]
            #gray = 0.21*r + 0.72*g + 0.07*b
            gray_image[i, j, 0] = 0.21*r
            gray_image[i, j, 1] = 0.72*g
            gray_image[i, j, 2] = 0.07*b
            

    gray_image = gray_image.astype("uint8")

    # *** DELETE LATER
    image = Image.fromarray(gray_image)
    image.save("rain_grayscale_cython.jpg")

    return gray_image

im = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
resized = im.resize((im.width // 2, im.height // 2))
pixels = np.asarray(resized)

run = cython_color2gray(pixels)

def cython_color2sepia(image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    ...
