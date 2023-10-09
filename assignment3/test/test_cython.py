import numpy.testing as nt
from in3110_instapy.cython_filters import cython_color2gray, cython_color2sepia
import numpy as np


def test_color2gray(image, reference_gray):
    """Test function for color2gray in cython implementation

    We check that the output image of the cython color2gray is the same shape
    as the python color2gray.

    We check that the output image is of type uint8.

    We chech that the filter is applying as it should by comparing some pixels in the output filtered image
    with the reference python image.

    Args:
        image  (ndarray): the input image that will run in cython_color2gray
        reference_gray  (ndarray): the output from the python_color2gray
    Returns:
        None
    """        



    gray_image = cython_color2gray(image)

    # Check if shapes match
    assert gray_image.shape == reference_gray.shape, "The resulting image has the wrong shape"

    # Check if the dtype is uint8
    assert gray_image.dtype == np.uint8, f"The type of {gray_image} is not an array of type uint8"
    
    # Checking if some selected pixels match
    assert np.allclose(gray_image[0, 0], reference_gray[0, 0], atol=1), f"The gray filter does not pass the test, the filter is not applying as it should"


def test_color2sepia(image, reference_sepia):
    """Test function for color2sepia in cython implementation

    We check that the output image of the cython color2sepia is the same shape
    as the python color2sepia.

    We check that the output image is of type uint8.

    We chech that the filter is applying as it should by comparing some pixels in the output filtered image
    with the reference python image.

    Args:
        image  (ndarray): the input image that will run in cython_color2sepia
        reference_sepia  (ndarray): the output from the python_color2sepia
    Returns:
        None
    """    

    sepia_image = cython_color2sepia(image)

    # Check if shapes match
    assert sepia_image.shape == reference_sepia.shape, "The resulting image has the wrong shape"

    # Check if the dtype is uint8
    assert sepia_image.dtype == np.uint8, f"The type of {sepia_image} is not an array of type uint8"

    # Checking if some selected pixels match
    assert np.allclose(sepia_image[0, 0], reference_sepia[0, 0], atol=1),  f"The sepia filter does not pass the test, the filter is not applying as it should"

