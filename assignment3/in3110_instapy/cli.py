"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys
import timeit

import in3110_instapy
import numpy as np
from PIL import Image
from in3110_instapy import python_filters, numba_filters, cython_filters, numpy_filters
from in3110_instapy.timing import time_one

from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python", # "numpy", "numba", "cython",
    filter: str = "color2gray", # "color2sepia",
    scale: int = 1,
    ) -> None:

    """Run the selected filter"""
    # load the image from a file
    jpg = Image.open(file)
    image = np.asarray(jpg)

    if scale != 1:
        # Resize image, if needed
        image = image.resize((image.width // scale, image.height // scale))

    # Apply the filter
    implementation_filter =  getattr(getattr(in3110_instapy, implementation+"_filters"), implementation+'_'+filter)
    filtered = implementation_filter(np.array(image))
    
    # Error message if illegal implementation used
    if implementation not in ["python", "numpy", "numba", "cython"]:
        raise ValueError("Implementation must be either python, numpy, numba or cython.")
    
    if out_file:
        # save the file
        Image.fromarray(filtered).save(out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument( "-h" "--help", action='help')
    
    parser.add_argument("file", help = "The filename to apply filter to")
    parser.add_argument("-o", "--out", help = "The output filename")

    # Add required arguments
    parser.add_argument("--gray", "-g", type=str, help = "Select a gray filter")
    parser.add_argument("--sepia", "-s", type=str, help = "Select a sepia filter")

    parser.add_argument("-sc", "--scale", type = int, default = 1, help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation", type=str, default = "python", choices = ["python", "numba", "numpy", "cython"], help = "The implementation")

    parser.add_argument("--runtime", "-r", type=bool, help = "Gives average runtime over 3 runs")
    arg = parser.parse_args()


    # Picking which filter to use, making gray the default filter
    if arg.sepia:
        chosen_filter = "color2sepia"
    else:
        chosen_filter = "color2gray" 

    # parse arguments and call run_filter
   

    def function():
        run_filter(
            arg.file,
            out_file=arg.out,
            implementation=arg.implementation,
            filter=chosen_filter,
            scale=arg.scale,)
    
    function()
    
    if arg.runtime:
        runtime = timeit.timeit(function, number=3)/3
        print(f"Average time over 3 runs: {runtime}s")

