cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project (pycinterface)
set(CMAKE_BUILD_TYPE Release)

set (SOURCES pycinterface.cpp)

set (HEADERS ImageTypes.h
             OsDetection.h)
add_library(pycinterface SHARED ${SOURCES} ${HEADERS})

add_custom_command(TARGET pycinterface POST_BUILD COMMAND python ARGS wrapper_code_generation.py ${CMAKE_SOURCE_DIR}/pycinterface.cpp ${CMAKE_BINARY_DIR} pycinterface VERBATIM WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})



