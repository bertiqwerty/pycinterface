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


# currently supported return values have a value different from None
_interfacing_types = {
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
    names for the function names in the cpp-interface file. If a Python wrapper function shall return the output buffer,
    the corresponding parameter has to be preceded by the _OUT_BUFFER_KEYWORD in the C++ file. In this case, we assume
    the parameter is a numpy array. The shape and the dtype will be taken from the first input parameter.
    """

    _OUT_BUFFER_KEYWORD = "OUT"

    with open(c_interface_file, "r") as f:
        # read file and remove comments
        content = "\n".join([c.split("//")[0] for c in re.sub("/\*.*?\*/", "",  f.read(), flags=re.DOTALL).split("\n")])

    function_signatures = [x for x in re.findall("DLL_EXPORT.+?\)", content, flags=re.DOTALL)]
    function_dict = OrderedDict()
    for sig in function_signatures:
        params_regex = re.compile("\(.*?\)", flags=re.DOTALL)
        # find function name
        wo_params = re.sub(params_regex, "", sig)
        tokens = re.split("\s", wo_params)
        name = tokens[-1]
        function_dict[name] = dict()

        # find return type and initialize dict
        function_dict[name] = {"restype": " ".join(tokens[1:-1]), "params": [], "out_buffers": []}

        # find parameters, remove template specifiers, and split at commas
        param_fields = re.sub("<.*?>", "", re.search(params_regex, sig).group(0)[1:-1]).split(",")

        out_buffer_indices = [i for i, s in enumerate(param_fields)
                              if _OUT_BUFFER_KEYWORD in [x.strip() for x in s.split(" ")]]

        name_position = -1  # last position in C++ should contain the name of the variable
        all_parameters = [re.search("[A-Za-z0-9_]+", x[name_position].strip()).group(0)
                          for x in (re.split("\s", s) for s in param_fields)]

        for i, p in enumerate(all_parameters):
            if i in out_buffer_indices:
                function_dict[name]["out_buffers"].append(p)
            else:
                function_dict[name]["params"].append(p)

    return function_dict


def generate_wrapper(in_file, base_folder, lib_name):
    """
    @brief Generates a string of native code wrappers in Python for a given C/C++-file
    """
    py_lib_var_name = "_"+ lib_name + "_native_lib"

    lib_wrapper = py_lib_var_name + " = NativeLibraryWrapper('" + base_folder+ "', '" + lib_name + "')\n\n\n"

    def func_str_gen(function_dict):
        for name in function_dict:
            func_str = "def " + name + "(" + ", ".join(function_dict[name]["params"] + [s + "=None" for s in function_dict[name]["out_buffers"]]) + "):\n"
            tab = " " * 4

            for buffer in function_dict[name]["out_buffers"]:
                func_str += tab + "if " + buffer + " is None:\n"
                func_str += tab * 2 + buffer + " = np.zeros_like(" + function_dict[name]["params"][0] + ")\n"

            if function_dict[name]["restype"] == "void":
                func_str += tab + py_lib_var_name + "." + name + "(" \
                                 + ", ".join(function_dict[name]["params"] + function_dict[name]["out_buffers"]) + ")\n"
            else:
                restype_str = _interfacing_types[function_dict[name]["restype"]]
                func_str += tab + py_lib_var_name + "." + name + ".restype = " + restype_str + "\n"
                func_str += tab + "return " + py_lib_var_name + "." + name + "(" + ", ".join(function_dict[name]["params"]) + ")\n"

            if len(function_dict[name]["out_buffers"]) > 0:
                func_str += tab + "return " + ", ".join(function_dict[name]["out_buffers"]) + "\n"
            yield func_str
    return lib_wrapper + "\n\n".join(func_str_gen(parse_c_interface(in_file)))


def generate_all_wrappers(cpp_files, base_folders, lib_names, out_file="native.py"):
    """
    Based on parsing the interface-c-files of our native code, this function generates corresponding Python
    wrappers for the passed project dict and writes the result to the given out_file.
    """
    wrapper_str = '# coding: utf-8\n"""\nThis file is auto-generated.\n"""\nimport ctypes\n'
    wrapper_str += "import numpy as np\n"
    wrapper_str += "from native_library_wrapper import NativeLibraryWrapper\n\n"

    for cpp_file, base_folder, lib_name in zip(cpp_files, base_folders, lib_names):
        wrapper_str += generate_wrapper(cpp_file, base_folder, lib_name) + "\n"
    with open(out_file, "w") as f:
        f.write(wrapper_str)


if __name__ == "__main__":
    # 1: c-file to be parsed, 2: base folder to look for library, 3: library name
    generate_all_wrappers([sys.argv[1]], [sys.argv[2]], [sys.argv[3]])
