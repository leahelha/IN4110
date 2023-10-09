from __future__ import annotations
"""
Profiling (IN4110 only)
"""
import cProfile
import pstats

import in3110_instapy
import line_profiler
import numpy as np
#from in3110_instapy import python_filters, numba_filters, cython_filters, numpy_filters
from in3110_instapy.io import random_image


def profile_with_cprofile(filter, image, ncalls=3):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    
    profiler = cProfile.Profile()
    # run `filter(image)` in the profiler

    profiler.enable()
    for i in range(ncalls):
        filter(image)
    profiler.disable()
        
    
    
    # print the top 10 results, sorted by cumulative time
    # (check sort_stats and print_stats docstrings)
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(10)


  

def profile_with_line_profiler(filter, image, ncalls=3):
    """Profile filter(image) with line_profiler

    Statistics will be printed to stdout.

    Args:

        filter (callable): filter function
        image (ndarray): image to filter
        ncalls (int): number of repetitions to measure
    """
    # create the LineProfiler
    profiler = line_profiler.LineProfiler()
    # tell it to measure the function we are given
    profiler.add_function(filter)

    # Measure filter(image)
    for i in range(ncalls):
        profiler(filter)(image)
       
    
    # print statistics
    profiler.print_stats()

def run_profiles(profiler: str = "cprofile"):
    """Run profiles of every implementation

    Args:

        profiler (str): either 'line_profiler' or 'cprofile'
    """
    if profiler == "cprofile":
        profile_func = profile_with_cprofile #profile_with_cprofile(filter, image)
    elif profiler == "line_profiler":
        profile_func = profile_with_line_profiler #profile_with_line_profiler(filter, image)
    else:
        raise ValueError(f"{profiler=} must be 'line_profiler' or 'cprofile'")
    
    
    # construct a random 640x480 image
    image = np.random.randint(0, 255, size=(640, 480, 3), dtype=np.uint8)#random_image(640, 480)

    filter_names = ["color2gray", "color2sepia"]  
    implementations = ["python", "numpy", "numba", "cython"] 

    for filter_name in filter_names:
        for implementation in implementations:
            print(f"Profiling {implementation} {filter_name} with {profiler}:")
            filter = in3110_instapy.get_filter(filter_name, implementation) #getattr(getattr(in3110_instapy, implementation+"_filters"), implementation+'_'+filter_name)

            # call it once
            filter(image)
            profile_func(filter, image)
            

                    
            
def main():
    print("Begin cProfile")
    run_profiles("cprofile")
    print("End cProfile")
    print('\n')
    print("Begin line_profiler")
    run_profiles("line_profiler")
    print("End line_profiler")

if __name__ == "__main__":
    main()
