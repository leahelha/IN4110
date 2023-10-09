from __future__ import annotations

import time
from typing import Callable
from PIL import Image
#from . import get_filter, io
import timeit
import numpy as np
import in3110_instapy
from in3110_instapy import python_filters, numba_filters, cython_filters, numpy_filters


def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    call = lambda: filter_function(*arguments)
    # return the _average_ time of one call
    avg_time = timeit.timeit(call, number=calls)/calls
    
    return avg_time





def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = Image.open(filename)
    im_array = np.asarray(image)
    # iterate through the filters
    filter_names = ["_color2gray", "_color2sepia"] #python, numpy, numba, cython
    K = 3  # number of calls

    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = python_filters.python_color2gray #...
        # time the reference implementation
        reference_time = time_one(reference_filter, im_array, calls = K)
        
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations = [ "cython", "numba", "numpy"]
        for implementation in implementations:
            filter = getattr(getattr(in3110_instapy, implementation+"_filters"), implementation+filter_name)#float(implementation)
            print(filter)
            # time the filter
            filter_time = time_one(filter, im_array, calls = K)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation}{filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )


if __name__ == "__main__":
    # run as `python -m in3110_instapy.timing`
    make_reports()
