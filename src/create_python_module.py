# coding: utf-8
"""
@author behrang
@file
@date Oct 13, 2016
@details Parser for the cpp-interface file to create Python wrappers
"""

from collections import OrderedDict
import re
import sys
import numpy as np

# currently supported return values have a value different from None
_interfacing_types = {
    "Imterface<float32>": "get_c_image_type(np.float32)",
    "Imterface<uint8>": "get_c_image_type(np.uint8)",
    "uint8": "ctypes.c_uint8",
    "int": "ctypes.c_int",
    "float32": "ctypes.c_float",
    "void": None,
    "double": "ctypes.c_double",
    "float": "ctypes.c_float"
}


def parse_c_interface(c_interface_file):
    """
    @brief Parses a c-interface file and generates a dictionary of function names to parameter lists.
    Exported functions are expected to be preceded by 'DLL_EXPORT'. Python keywords should not be used as variable
    names for the function names in the cpp-interface file.
    """
    with open(c_interface_file, "r") as f:
        content = f.read()

    content = re.sub("/\*.*?\*/", "", content, flags=re.DOTALL)
    content = "\n".join([c.split("//")[0] for c in content.split("\n")])

    function_signatures = [x for x in re.findall("DLL_EXPORT.+?\)", content, flags=re.DOTALL)]
    function_dict = OrderedDict()
    for sig in function_signatures:
        params_regex = re.compile("\(.*?\)", flags=re.DOTALL)
        # find function name
        wo_params = re.sub(params_regex, "", sig)
        tokens = re.split("\s", wo_params)
        name = tokens[-1]
        function_dict[name] = dict()

        # find return type
        returns_imterface = re.search("Imterface<.*?>", wo_params, flags=re.DOTALL)
        if returns_imterface is not None:
            function_dict[name]["restype"] = returns_imterface.group(0)
        else:
            function_dict[name]["restype"] = " ".join(tokens[1:-1])

        # find parameters
        param_string = re.search(params_regex, sig).group(0)[1:-1]
        param_string = re.sub("<.*?>", "", param_string) # remove template specifiers
        parameters = [ re.search("[A-Za-z0-9_]+",x[-1].strip()).group(0) for x in  [re.split("\s", s) for s in param_string.split(",")]]
        function_dict[name]["params"] = parameters

    return function_dict


def cpp_file_to_py_file_content(in_file, base_folder, lib_name):
    """
    @brief Generates native code wrapping strings in Python
    """
    dc_functions = parse_c_interface(in_file)
    lib_wrapper = "_"+lib_name + "_native_lib"
    functions_str = lib_wrapper + " = NativeLibraryWrapper('" + base_folder+ "', '" + lib_name + "')\n\n\n"
    for name in dc_functions:
        functions_str += "def " + name + "(" + ", ".join(dc_functions[name]["params"]) + "):\n"
        restype_str = _interfacing_types[dc_functions[name]["restype"]]
        if restype_str is not None:
            functions_str += "    " + lib_wrapper + "." + name + ".restype = " + restype_str + "\n"
        functions_str += "    return " + lib_wrapper + "." + name \
                         + "(" + ", ".join(dc_functions[name]["params"]) + ")\n\n\n"
    return functions_str


def generate_python_wrapper(cppfiles, base_folders, lib_names, out_file="native.py"):
    """
    @brief Based on parsing the interface-c-files of our native code, this function generates corresponding Python
    wrappers for the passed project dict and writes the result to the given out_file.
    """
    wrapper_str = "import ctypes\n"
    wrapper_str += "import numpy as np\n"
    wrapper_str += "from native_library_wrapper import NativeLibraryWrapper, get_c_image_type\n\n"

    for cpp_file, base_folder, lib_name in zip(cppfiles, base_folders, lib_names):
        wrapper_str += cpp_file_to_py_file_content(cpp_file, base_folder, lib_name) + "\n"
    with open(out_file, "w") as f:
        f.write(wrapper_str)


if __name__ == "__main__":
    # 1: c-file to be parsed, 2: base folder to look for library, 3: library name
    generate_python_wrapper([sys.argv[1]], [sys.argv[2]],  [sys.argv[3]])
