# coding: utf-8
"""
@author behrang
@file
@date Oct 13, 2016
@details Parser for the cpp-interface file to create Python wrappers
"""

import nltk
import re


def parse_c_interface(c_interface_file):
    """
    @brief Parses a c-interface file and generates a dictionary of function names to parameter lists.
    Exported functions are expected to be preceded by 'DLL_EXPORT'. Python keywords should not be used as variable
    names for the function names in the cpp-interface file.
    """
    with open(c_interface_file, "r") as f:
        content = f.read()

    content = re.sub("Imterface<[_0-9a-zA-Z]+>", "", content)
    content = "\n".join([c.split("//")[0] for c in content.split("\n")])
    content = content.replace("uint8", "")
    content = content.replace("int", "")
    content = content.replace("float32", "")
    content = content.replace("void", "")
    content = content.replace("*", "")
    content = content.replace("lambda", "lambda_param")
    try:
        tokens = nltk.word_tokenize(content)
    except LookupError:
        nltk.download('punkt')
        tokens = nltk.word_tokenize(content)
    dc_functions = dict()
    for i, token in enumerate(tokens):
        if token == "DLL_EXPORT":
            final_index = i
            j = 1
            while True:
                if tokens[i + j] == ")":
                    final_index = i + j
                    break
                j += 1
            params = [p for p in tokens[i+3:final_index:2]]
            function_name = tokens[i + 1]
            dc_functions[function_name] = params
    return dc_functions


def cpp_file_to_py_file_content(in_file, base_folder, lib_name):
    """
    @brief Generates native code wrapping strings in Python
    """
    dc_functions = parse_c_interface(in_file)

    functions_str = lib_name + "_native_lib = NativeLibraryWrapper('" + base_folder+ "', '" + lib_name + "')\n"
    for name in dc_functions:
        functions_str += "def " + name + "(" + ", ".join(dc_functions[name]) + "):\n"
        functions_str += "    return " + lib_name + "_native_lib." + name \
                         + "(" + ", ".join(dc_functions[name]) + ")\n"
    return functions_str


def generate_python_wrapper(cppfiles, base_folders, lib_names, out_file="native.py"):
    """
    @brief Based on parsing the interface-c-files of our native code, this function generates corresponding Python
    wrappers for the passed project dict and writes the result to the given out_file.
    """
    wrapper_str = "from native_library_wrapper import NativeLibraryWrapper\n\n"

    for cppfile, base_folder, lib_name in zip(cppfiles, base_folders, lib_names):
        wrapper_str += cpp_file_to_py_file_content(cppfile, base_folder, lib_name) + "\n"
    with open(out_file, "w") as f:
        f.write(wrapper_str)


if __name__ == "__main__":
    generate_python_wrapper(["pycinterface.cpp"], [".."],  ["pycinterface"])