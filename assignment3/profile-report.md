# Profiling report

## Questions

A few questions below. We are not asking for lots of detail,
just 1-2 sentences each.

### Question 1

> which profiler produced the most useful output, and why?

The cProfile profiler appears to have been the most useful profiler, as it provided detailed information about the function calls, cumulative time, and per-call time and didn't fail.
Line_profiler couldn't give any output for the numba or cython implementations (this could be due to improper implementation on my part), making cProfiler the winner.




### Question 2

> Which implementations have the most useful profiling output, and why?

The most useful profiling output was obtained for the python_color2gray and numpy_color2gray implementations in both profiling methods. 
cProfile showed a breakdown of the function calls, cumulative time, and per-call time, offering insights into their performance and line_profiler gave.

### Question 3

> Do any profiler+implementations produce seem to not work at all? If so, which?

Both profilers seemed to struggle with the numba and the cython implementation, particulary line_profiler which got an AttributeError for the cython_color2gray filter.
Line_profiler never got to the sepia filters as it recieved an error message for the first cython filter, it failed at numba and cython.

## profile output

<details>
<summary>cProfile output</summary>

```
Begin cProfile
Profiling python color2gray with cprofile:
         28 function calls in 5.263 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    5.263    1.754    5.263    1.754 python_filters.py:9(python_color2gray)
        3    0.000    0.000    0.000    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        6    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(shape)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1965(shape)
        3    0.000    0.000    0.000    0.000 multiarray.py:80(empty_like)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1961(_shape_dispatcher)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numpy color2gray with cprofile:
         8294428 function calls in 8.903 seconds

   Ordered by: cumulative time
   List reduced from 11 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    2.873    0.958    8.903    2.968 numpy_filters.py:8(numpy_color2gray)
  2764800    1.158    0.000    6.029    0.000 <__array_function__ internals>:177(dot)
  2764806    4.594    0.000    4.594    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
  2764800    0.277    0.000    0.277    0.000 multiarray.py:736(dot)
        3    0.000    0.000    0.000    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(shape)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1965(shape)
        3    0.000    0.000    0.000    0.000 multiarray.py:80(empty_like)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1961(_shape_dispatcher)


Profiling numba color2gray with cprofile:
         7 function calls in 0.007 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.007    0.002    0.007    0.002 numba_filters.py:9(numba_color2gray)
        3    0.000    0.000    0.000    0.000 serialize.py:29(_numba_unpickle)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling cython color2gray with cprofile:
         4 function calls in 0.366 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.366    0.122    0.366    0.122 cython_filters.py:26(cython_color2gray)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling python color2sepia with cprofile:
         2764828 function calls in 17.942 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3   17.361    5.787   17.942    5.981 python_filters.py:38(python_color2sepia)
  2764800    0.581    0.000    0.581    0.000 {built-in method builtins.min}
        3    0.000    0.000    0.000    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        6    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(shape)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1965(shape)
        3    0.000    0.000    0.000    0.000 multiarray.py:80(empty_like)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1961(_shape_dispatcher)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling numpy color2sepia with cprofile:
         11059231 function calls in 9.643 seconds

   Ordered by: cumulative time
   List reduced from 13 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    3.840    1.280    9.643    3.214 numpy_filters.py:36(numpy_color2sepia)
  2764800    1.351    0.000    5.242    0.000 <__array_function__ internals>:177(dot)
  2764806    3.575    0.000    3.575    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
  2764800    0.560    0.000    0.560    0.000 {built-in method builtins.min}
  2764800    0.316    0.000    0.316    0.000 multiarray.py:736(dot)
        3    0.000    0.000    0.000    0.000 {method 'astype' of 'numpy.ndarray' objects}
        3    0.000    0.000    0.000    0.000 {built-in method numpy.array}
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(empty_like)
        3    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(shape)
        3    0.000    0.000    0.000    0.000 fromnumeric.py:1965(shape)


Profiling numba color2sepia with cprofile:
         7 function calls in 0.017 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3    0.017    0.006    0.017    0.006 numba_filters.py:35(numba_color2sepia)
        3    0.000    0.000    0.000    0.000 serialize.py:29(_numba_unpickle)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Profiling cython color2sepia with cprofile:
         40 function calls in 15.524 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        3   15.524    5.175   15.524    5.175 cython_filters.py:59(cython_color2sepia)
        9    0.000    0.000    0.000    0.000 <__array_function__ internals>:177(shape)
        9    0.000    0.000    0.000    0.000 {built-in method numpy.core._multiarray_umath.implement_array_function}
        9    0.000    0.000    0.000    0.000 fromnumeric.py:1965(shape)
        9    0.000    0.000    0.000    0.000 fromnumeric.py:1961(_shape_dispatcher)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


End cProfile

```

</details>

<details>
<summary>line_profiler output</summary>

```

Begin line_profiler
Profiling python color2gray with line_profiler:
Timer unit: 1e-09 s

Total time: 1.91326 s
File: /Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/python_filters.py
Function: python_color2gray at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           def python_color2gray(image: np.array) -> np.array:
    10                                               """Convert rgb pixel array to grayscale
    11                                           
    12                                               Args:
    13                                                   image (np.array)
    14                                               Returns:
    15                                                   np.array: gray_image
    16                                               """
    17                                           
    18         1       8000.0   8000.0      0.0      gray_image = np.empty_like(image) #(H W C)
    19                                               
    20                                               # iterate through the pixels, and apply the grayscale transform   
    21                                               # Separating the image dimensions into height width and color 
    22         1       5000.0   5000.0      0.0      h, w, c = np.shape(image)
    23                                           
    24                                           
    25       641     228000.0    355.7      0.0      for i in range(h):
    26    307840   98373000.0    319.6      5.1          for j in range(w):
    27                                                       # # Make image gray, and save in gray_image  
    28    307200 1814564000.0   5906.8     94.8              gray_image[i,j] = image[i,j,0]*0.21 + image[i,j,1]*0.72 + image[i,j,2]*0.07
    29                                           
    30                                               
    31         1      82000.0  82000.0      0.0      gray_image = gray_image.astype("uint8")
    32                                           
    33                                           
    34         1       1000.0   1000.0      0.0      return gray_image

Profiling numpy color2gray with line_profiler:
Timer unit: 1e-09 s

Total time: 4.41003 s
File: /Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/numpy_filters.py
Function: numpy_color2gray at line 8

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           def numpy_color2gray(image: np.array) -> np.array:
     9                                               """Convert rgb pixel array to grayscale
    10                                           
    11                                               Args:
    12                                                   image (np.array)
    13                                               Returns:
    14                                                   np.array: gray_image
    15                                               """
    16                                           
    17         1       8000.0   8000.0      0.0      gray_image = np.empty_like(image)
    18         1       4000.0   4000.0      0.0      h, w, c = np.shape(image)
    19                                               # Converting the original image to grayscale
    20       641     215000.0    335.4      0.0      for i in range(h):
    21    307840   99815000.0    324.2      2.3          for j in range(w):
    22   1228800  504168000.0    410.3     11.4              for k in range(c):
    23    921600 3186849000.0   3458.0     72.3                  gray = np.dot(image[i,j,:],[0.21, 0.72, 0.07])
    24    921600  618898000.0    671.5     14.0                  gray_image[i,j,k] = gray
    25                                                           
    26                                               
    27                                               # Hint: use numpy slicing in order to have fast vectorized code
    28                                               
    29                                               # Return image (make sure it's the right type!)
    30         1      75000.0  75000.0      0.0      gray_image = gray_image.astype("uint8")
    31                                           
    32         1          0.0      0.0      0.0      return gray_image

Profiling numba color2gray with line_profiler:
/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/profiling.py:61: UserWarning: Adding a function with a __wrapped__ attribute. You may want to profile the wrapped function by adding numba_color2gray.__wrapped__ instead.
  profiler.add_function(filter)
/Users/lh/opt/anaconda3/envs/comap1/lib/python3.10/site-packages/line_profiler/line_profiler.py:75: UserWarning: Adding a function with a __wrapped__ attribute. You may want to profile the wrapped function by adding numba_color2gray.__wrapped__ instead.
  self.add_function(func)
Timer unit: 1e-09 s

Total time: 0 s
File: /Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/numba_filters.py
Function: numba_color2gray at line 9

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     9                                           @jit(nopython=True)
    10                                           def numba_color2gray(image: np.array) -> np.array:
    11                                               """Convert rgb pixel array to grayscale
    12                                           
    13                                               Args:
    14                                                   image (np.array)
    15                                               Returns:
    16                                                   np.array: gray_image
    17                                               """
    18                                               gray_image = np.empty_like(image)
    19                                               
    20                                               # iterate through the pixels, and apply the grayscale transform
    21                                               h, w, c = np.shape(image)
    22                                           
    23                                               for i in range(h):
    24                                                   for j in range(w):
    25                                                       # Make image gray, and save in gray_image
    26                                                       gray_image[i,j] = image[i,j,0]*0.21 + image[i,j,1]*0.72 + image[i,j,2]*0.07
    27                                           
    28                                               
    29                                               gray_image = gray_image.astype("uint8")
    30                                           
    31                                           
    32                                               return gray_image

Profiling cython color2gray with line_profiler:
Traceback (most recent call last):
  File "line_profiler/_line_profiler.pyx", line 252, in line_profiler._line_profiler.LineProfiler.add_function
AttributeError: attribute '__code__' of '_cython_3_0_2.cython_function_or_method' objects is not writable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/lh/opt/anaconda3/envs/comap1/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Users/lh/opt/anaconda3/envs/comap1/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/profiling.py", line 114, in <module>
    main()
  File "/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/profiling.py", line 110, in main
    run_profiles("line_profiler")
  File "/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/profiling.py", line 99, in run_profiles
    profile_func(filter, image)
  File "/Users/lh/Documents/Uni/IN4110/IN3110-leaheh/assignment3/in3110_instapy/profiling.py", line 65, in profile_with_line_profiler
    profiler(filter)(image)
  File "/Users/lh/opt/anaconda3/envs/comap1/lib/python3.10/site-packages/line_profiler/line_profiler.py", line 75, in __call__
    self.add_function(func)
  File "line_profiler/_line_profiler.pyx", line 208, in line_profiler._line_profiler.LineProfiler.add_function
  File "line_profiler/_line_profiler.pyx", line 254, in line_profiler._line_profiler.LineProfiler.add_function
AttributeError: '_cython_3_0_2.cython_function_or_method' object has no attribute '__func__'. Did you mean: '__doc__'?
```

</details>
