from cython_filters import cython_color2gray, cython_color2sepia
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
def cython_test():
    """
    Test function to see if cython_color2gray in cython_filters will produce a grayscaled image
    """
    image = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
    pixels = np.asarray(image)
    sepia= cython_color2sepia(pixels)
    sepia_image = Image.fromarray(sepia)
    sepia_image.show()

    return

run = cython_test()