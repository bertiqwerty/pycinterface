# pycinterface
Lightweight interface between Python and C/C++ with a focus on images as numpy arrays based on ctypes

To compile the test example,
create a build ordner, e.g., in ```pycinterface/build```. Execute ```cmake ../src``` from within ```pycinterface/build```. Go to the ```pycinterface/src``` and execute ```python test_pycinterface.py```.

Functions exported from a C/C++ library can be called from Python with the Python package ```ctypes```. This library provides a wrapper based on ```ctypes``` that makes passing of image data with numpy arrays convenient. See ```src/test_pycinterface.py``` for more information on how to call your library functions. ```src/pycinterface.cpp``` shows an example of a C++ library. Important is the ```DLL_EXPORT``` macro before the function definitions. Renaming the macro will lead to problems when creating the Python wrappers. 
