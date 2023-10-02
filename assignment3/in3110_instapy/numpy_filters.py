"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np
from PIL import Image
"""
  gray_image = np.empty_like(image) #(H W C)
    
    # iterate through the pixels, and apply the grayscale transform    
    h, w, c = np.shape(image)

    for i in range(h):
        for j in range(w):
            #for k in range(c):
            # Separate RGB values from image
            r, g, b = image[i, j, :]

            # Make image gray, and save in gray_image
            gray = 0.21*r + 0.72*g + 0.07*b
            
            gray_image[i,j, :] = gray

    
    grayscale_array = gray_image.astype("uint8")

    
    image = Image.fromarray(grayscale_array)
    image.save("rain_grayscale.jpg")
"""

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    # Converting the original image to grayscale
    gray_convert = np.dot(image[:,:,:3],[0.21, 0.72, 0.07])

    gray_image = gray_convert
    
    # Hint: use numpy slicing in order to have fast vectorized code
    
    # Return image (make sure it's the right type!)
    gray_image = gray_image.astype("uint8")

    # *** DELETE LATER
    image = Image.fromarray(gray_image)
    image.save("rain_grayscale.jpg")

    return gray_image

# *** DELETE LATER
im = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
resized = im.resize((im.width // 2, im.height // 2))
pixels = np.asarray(resized)

run = numpy_color2gray(pixels)

def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
        you may ignore it)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = ...

    # define sepia matrix (optional: with stepless sepia changes)
    sepia_matrix = ...

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    sepia_image = ...

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    ...

    # Return image (make sure it's the right type!)
    return sepia_image
