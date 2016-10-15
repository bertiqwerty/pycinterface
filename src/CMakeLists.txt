cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project (pycinterface)
set(CMAKE_BUILD_TYPE Release)

set (SOURCES pycinterface.cpp)

set (HEADERS ImageTypes.h
             OsDetection.h)
add_library(pycinterface SHARED ${SOURCES} ${HEADERS})

set_property(TARGET pycinterface PROPERTY CXX_STANDARD 14)

add_custom_command(TARGET pycinterface POST_BUILD COMMAND python ARGS -c "import os; os.chdir('${CMAKE_SOURCE_DIR}'); exec(open('create_python_module.py').read())" VERBATIM)



