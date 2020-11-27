# Pycinterface
Pycinterface is a lightweight interface between Python and C/C++ with a focus on images as numpy arrays based on ctypes (https://docs.python.org/3/library/ctypes.html).

## Introduction

To compile the test example,
create w.l.o.g. a build folder in ```pycinterface/build```. Execute ```cmake ..``` from within ```pycinterface/build```. Then, you can compile the code, e.g., with ```cmake --build . --config Release```. Go to ```pycinterface``` and execute ```python test_pycinterface.py``` to see if everything works.

Functions exported from a dynamic C/C++ library can be called from Python with the Python package ```ctypes```. Pycinterface provides a wrapper around ```ctypes``` that makes passing of image data with numpy arrays convenient. See ```test_pycinterface.py``` for more information on how to call your C/C++ library functions from Python. ```pycinterface.cpp``` shows an example of a C++ library. Important is the ```DLL_EXPORT``` macro before the function definitions. Renaming or removing the macro will lead to problems when creating the Python wrappers. 

## Basic Example

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

## Return Values

You can return primitives without restrictions. To this end, you have to add the Python type and the ```ctypes``` type to the dict 
```
# currently supported return values have a value different from None
_interfacing_types = {
    "uint8": "ctypes.c_uint8",
    "int": "ctypes.c_int",
    "float32": "ctypes.c_float",
    "void": None,
    "double": "ctypes.c_double",
    "float": "ctypes.c_float"
}
```

in [```wrapper_code_generation.py```](wrapper_code_generation.py) if not yet available. For ```numpy``` arrays that require data allocation, we do not support allocation in C/C++ and returning the pointer. However, you can let the Python function wrapper return the output buffer. Therefore, you have to add the macro ```OUT``` in front of the parameter in the c-function's signature such as
```
DLL_EXPORT void add_f(Imterface<float32> *im_in1, Imterface<float32> *im_in2, OUT Imterface<float32> *im_out)
{
    ...
}
```

The generated Python wrapper will look as follows 
```
def add_f(im_in1, im_in2, im_out=None):
    if im_out is None:
        im_out = np.zeros_like(im_in1)
    _pycinterface_native_lib.add_f(im_in1, im_in2, im_out)
    return im_out
```
By default, the first input parameter is expected to be a ```numpy``` array and the output array will have its size and data type. If you need an output buffer of a different type, you have to create one yourself.

