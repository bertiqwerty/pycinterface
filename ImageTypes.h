/**
 * @author behrang
 * @file
 * @date Oct 17, 2015
 * @details Image interface class
 */

#ifndef _IMAGE_TYPES_HPP_
#define _IMAGE_TYPES_HPP_


typedef float float32;
typedef double float64;
typedef unsigned char uint8;

/**
 * @details This class can be used for interfacing from other programming languages such as Python.
 * @tparam T    data type of the image elements
 */
template <class T>
struct Imterface
{
    T *data;
    int channels;
    int width;
    int height;
    int xStride;
    int yStride;
    int typeId;
};


template<class T>
struct ImageTypeTrait
{
    static int const value = -1;
};
template<> struct ImageTypeTrait<float32> { static int const value = 0; };
template<> struct ImageTypeTrait<uint8> { static int const value = 1; };
template<> struct ImageTypeTrait<float64> { static int const value = 2; };
template<> struct ImageTypeTrait<int> { static int const value = 3; };

template<typename T>
bool typeCheck(const Imterface<T>& im)
{
    return ImageTypeTrait<T>::value == im.typeId;
}

typedef Imterface<float32> Imterface_f32;

#endif
