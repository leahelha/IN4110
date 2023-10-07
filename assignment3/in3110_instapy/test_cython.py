from cython_filters import cython_color2gray
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
def cython_test():
    """
    Test function to see if cython_color2gray in cython_filters will produce a grayscaled image
    """
    image = Image.open("/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/test/rain.jpg")
    pixels = np.asarray(image)
    grayscale = cython_color2gray(pixels)
    gray_image = Image.fromarray(grayscale)
    # gray_image.show()

    return

run = cython_test()