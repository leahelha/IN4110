from in3110_instapy.python_filters import python_color2gray, python_color2sepia
import numpy as np


def test_color2gray(image):
    """Test function for color2gray in python implementation

    We check that the output image of the python color2gray is the same shape
    as the input image.

    We check that the output image is of type uint8.

    We chech that the filter is applying as it should by checking that all the pixels are uniform.

    Args:
        image (ndarray): the input image that will run in color2gray
    Returns:
        None
    """ 
    # run color2gray
    gray_image = python_color2gray(image)

    # check that the result has the right shape, type
    
    assert np.shape(gray_image)==np.shape(image), "The resulting image has the wrong shape"
    assert gray_image.dtype == np.uint8, f"The type of {gray_image} is not an array of type uint8"
    # assert uniform r,g,b values
    assert np.allclose(gray_image[:,:,0],gray_image[:,:,1]) and np.allclose(gray_image[:,:,1],gray_image[:,:,2]) and np.allclose(gray_image[:,:,0],gray_image[:,:,2]), f"RGB values are not uniform"


def test_color2sepia(image):
    """Test function for color2sepia in python implementation

    We check that the output image of the python color2gray is the same shape
    as the input image.

    We check that the output image is of type uint8.

    We chech that the filter is applying as it should by checking some of the pixels.
    We check by applying the filter in the test function to the same pixels and compare it with the function python_color2sepia.

    Args:
        image (ndarray): the input image that will run in python_color2sepia
    Returns:
        None
    """
    # run color2sepia
    im = image
    sepia_image = python_color2sepia(im)
    
    # check that the result has the right shape, type
    assert np.shape(sepia_image)==np.shape(im),"The resulting image has the wrong shape"
    assert sepia_image.dtype == np.uint8, f"The type of {sepia_image} is not an array of type uint8"
    # verify some individual pixel samples
    # according to the sepia matrix
    sepia_matrix = [
    [ 0.393, 0.769, 0.189],
    [ 0.349, 0.686, 0.168],
    [ 0.272, 0.534, 0.131]]

    sepia_test = np.zeros(3)
    for i in range(3):
        r, g, b = im[0, 0, :]
        sepi = r*sepia_matrix[i][0]+g*sepia_matrix[i][1]+b*sepia_matrix[i][2]
        sepia_test[i] = min(255, sepi)
    
    assert np.allclose(sepia_image[0,0,:],sepia_test[:], atol=1), f"The sepia filter does not pass the test, the filter is not applying as it should"

