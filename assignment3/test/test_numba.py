import numpy.testing as nt
from in3110_instapy.numba_filters import numba_color2gray, numba_color2sepia
import numpy as np



def test_color2gray(image, reference_gray):

    gray_image = numba_color2gray(image)
    
    # Check if shapes match
    assert gray_image.shape == reference_gray.shape, "The resulting image has the wrong shape"

    # Check if the dtype is uint8
    assert gray_image.dtype == np.uint8, f"The type of {gray_image} is not an array of type uint8"
    
    # Checking if some selected pixels match
    assert np.allclose(gray_image[0, 0], reference_gray[0, 0], atol=1), f"The gray filter does not pass the test, the filter is not applying as it should"





def test_color2sepia(image, reference_sepia):

    sepia_image = numba_color2sepia(image)
    
    # Check if shapes match
    assert sepia_image.shape == reference_sepia.shape, "The resulting image has the wrong shape"

    # Check if the dtype is uint8
    assert sepia_image.dtype == np.uint8, f"The type of {sepia_image} is not an array of type uint8"
    
    # Checking if some selected pixels match
    assert np.allclose(sepia_image[0, 0], reference_sepia[0, 0], atol=1), f"The sepia filter does not pass the test, the filter is not applying as it should"



