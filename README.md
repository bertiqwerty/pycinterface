# Pycinterface
Pycinterface is a lightweight interface between Python and C/C++ with a focus on images as numpy arrays based on ctypes (https://docs.python.org/3/library/ctypes.html).

## Introduction

To compile the test example,
create a build folder, e.g., in ```pycinterface/build```. Execute ```cmake ../src``` from within ```pycinterface/build```. Then, you can compile the code, e.g., with ```cmake --build . --config Release```. Go to ```pycinterface/src``` and execute ```python test_pycinterface.py``` to see if everything works.

Functions exported from a dynamic C/C++ library can be called from Python with the Python package ```ctypes```. Pycinterface provides a wrapper around ```ctypes``` that makes passing of image data with numpy arrays convenient. See ```src/test_pycinterface.py``` for more information on how to call your C/C++ library functions from Python. ```src/pycinterface.cpp``` shows an example of a C++ library. Important is the ```DLL_EXPORT``` macro before the function definitions. Renaming or removing the macro will lead to problems when creating the Python wrappers. 

Note: Currently, returning values is not supported. You have to pass output buffers to the C/C++ functions.

## Example

A function ```dummy_f``` exported from your library via
```
#include "ImageTypes.h"
#include "OsDetection.h"

DLL_EXPORT void dummy_f(Imterface<float>* im)
{
    // manipulate im somehow
}
```
can be called from Python as follows.
```
import native
import numpy as np

im=np.zeros((100, 100), dtype=np.float32)
native.dummy_f(im)
```
