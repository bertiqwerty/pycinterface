# coding: utf-8
"""
@author behrang
@file
@date Aug 29, 2015
@details Wrapper for native libraries with c-style interface
"""

import ctypes
import numpy as np
import os


def in_debug_mode():
    try:
        import pydevd
        debugging = True
    except ImportError:
        debugging = False

    return debugging


# All supported numpy dtypes and there ctype counter parts are defined manually in this dict.
_np_dtype_2_ctype_p = {
    np.dtype(np.float32): ctypes.POINTER(ctypes.c_float),
    np.dtype(np.uint8): ctypes.POINTER(ctypes.c_uint8),
    np.dtype(np.float64): ctypes.POINTER(ctypes.c_double),
    np.dtype(np.int): ctypes.POINTER(ctypes.c_int),
}


# These type ids are used to check whether the correct function has been called in the cpp-lib
_np_dtype_2_type_id = {
    np.dtype(np.float32): 0,
    np.dtype(np.uint8): 1,
    np.dtype(np.float64): 2,
    np.dtype(np.int): 3,
}

# To not recreate already created types, they are stored in this dict and only created if not already existing.
_np_dtype_2_cimage = dict()


def get_c_image_type(np_dtype):
    """
    @brief Creates an image class that can be passed to C++ where an according struct has to be defined
    @param np_dtype data type of the numpy array representing the image in Python
    @return pointers of instances to this class can be passed to a C++ library
    """
    data_type = np_dtype

    if np.dtype(data_type) in _np_dtype_2_cimage:
        return _np_dtype_2_cimage[np.dtype(data_type)]
    else:

        class CImage(ctypes.Structure):
            _fields_ = [
                ("data", _np_dtype_2_ctype_p[data_type]),
                ("channels", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("xStridePix", ctypes.c_int),
                ("yStridePix", ctypes.c_int),
                ("typeId", ctypes.c_int)
            ]

            def __str__(self):
                return str(self._fields_)

        _np_dtype_2_cimage[np.dtype(data_type)] = CImage
        return CImage


# class NpCArray(np.array):
#
#     def __del__(self):
#         super(NpCArray, self).__del__()


class _FunctionWrapper:
    """
    Wrapper for functions exported by a dynamic library. Some arguments such as ints, floats and numpy arrays are
    converted automatically.
    """
    def __init__(self, function_name, library):
        self.name = function_name
        self.library = library
        self.restype = ctypes.c_int

    def __call__(self, *args):
        converted_args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, np.ndarray):
                c_image_type = get_c_image_type(arg.dtype)
                if len(arg.shape) == 3:
                    c_image = c_image_type(
                        arg.ctypes.data_as(_np_dtype_2_ctype_p[np.dtype(arg.dtype)]),
                        arg.shape[2], arg.shape[1], arg.shape[0],
                        arg.strides[1] // arg.itemsize, arg.strides[0] // arg.itemsize,
                        _np_dtype_2_type_id[np.dtype(arg.dtype)]
                    )
                elif len(arg.shape) == 2:
                    c_image = c_image_type(
                        arg.ctypes.data_as(_np_dtype_2_ctype_p[np.dtype(arg.dtype)]),
                        1, arg.shape[1], arg.shape[0],
                        arg.strides[1] // arg.itemsize, arg.strides[0] // arg.itemsize,
                        _np_dtype_2_type_id[np.dtype(arg.dtype)]
                    )

                converted_args[i] = ctypes.POINTER(c_image_type)(c_image)

            elif isinstance(arg, float):
                converted_args[i] = ctypes.c_float(arg)
            elif isinstance(arg, int):
                converted_args[i] = ctypes.c_int(arg)

        # retrieve function with ctypes
        c_func = getattr(self.library, self.name)
        c_func.restype = self.restype
        # call C/C++ function
        return c_func(*converted_args)


class NativeLibraryWrapper:
    """
    Wrapper for a dynamic library with automatic conversion of numpy arrays.
    """
    def __init__(self, base_folder, library_name, path_to_library=""):
        """
        Searches folders below base_folder for a library with name library_name
        @param base_folder: root folder to look for the library
        @param library_name: name of the library
        @param path_to_library: optional explicit path to library, if given, no search is executed.
        """

        if path_to_library == "":
            os_ending = {
                "nt": "dll",
                "posix": "so"
            }
            for os_name in os_ending:
                if os.name == os_name:
                    for root, dirs, files in os.walk(base_folder):
                        for f in files:
                            if in_debug_mode():
                                if library_name.lower() + "." + os_ending[os_name] in f.lower() and "Debug" in root:
                                    path_to_library = os.path.join(root, f)
                                    print("Found path " + path_to_library)

                            else:
                                if library_name.lower() + "." + os_ending[os_name] in f.lower() and "Debug" not in root:
                                    path_to_library = os.path.join(root, f)

        if path_to_library == "":
            raise IOError("Did not find library.")

        self.library = ctypes.cdll.LoadLibrary(path_to_library)
        self.functions = dict()

    def __getattr__(self, function):
        if function in self.functions:
            return self.functions[function]
        else:
            self.functions[function] = _FunctionWrapper(function, self.library)
            return self.functions[function]


if __name__ == "__main__":

    # Example (of course you have to build the cpp-lib beforehand):
    x = np.array([[2, 3, 4], [1, 2, 3]], dtype=np.float32)
    x_out = np.array([[2, 3, 4], [1, 2, 3]], dtype=np.float32)

    wrapper = NativeLibraryWrapper("build", "pycinterface")
    wrapper.add_f(x, x, x_out)
    print(x_out)

