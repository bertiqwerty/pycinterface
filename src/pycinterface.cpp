/**
 * @author behrang
 * @file
 * @date Oct 13, 2016
 * @details Example C++ library with interface to Python
 */

#include "OsDetection.h"
#include "ImageTypes.h"
#include <iostream>

template <typename T>
void clean_memory(Imterface<T> *im_in)
{
    delete[] im_in->data;
    delete im_in;
}

DLL_EXPORT void clean_memory_f(Imterface<float32> *im_in)
{
    clean_memory(im_in);
}
DLL_EXPORT void clean_memory_u8(Imterface<uint8> *im_in)
{
    clean_memory(im_in);
}



// Functions are made available in Python with the DLL_EXPORT macro.
//DLL_EXPORT void add_f(Imterface<float32> *im_in1, Imterface<float32> *im_in2)
DLL_EXPORT Imterface<float32>* add_f(Imterface<float32> *im_in1, Imterface<float32> *im_in2)
{
    std::cout << "HALLO" << std::endl;
    std::cout << im_in1->typeId << std::endl;

    // You probably don't want to use the Imterface instance directly but create an image class that checks
    // the type in its constructor, allocates memory without using 'new', and has convenient access operators.
    if (typeCheck(*im_in1) && typeCheck(*im_in2))
    {

        std::cout << "HALLO2" << std::endl;

        Imterface<float32> *im_out = new Imterface<float32>;
        *im_out = { nullptr, im_in1->channels, im_in1->width, im_in1->height, im_in1->channels, im_in1->width, im_in1->typeId };
        im_out->data = new float32[im_out->width * im_out->height];

        // You probably want to use templated functions for your algorithms and use this function only as interface.
        for (int y = 0; y < im_in1->height; y++)
        {
            for (int x = 0; x < im_in1->width; x++)
            {
                im_out->data[x * im_out->xStride + y * im_out->yStride] =
                        im_in1->data[x * im_in1->xStride + y * im_in1->yStride] + im_in2->data[x * im_in2->xStride + y * im_in2->yStride];
            }
        }
        return im_out;
    }
    else
    {
        std::cerr << "Wrong image data type!" << std::endl;
        return nullptr;
    }
}


DLL_EXPORT void threshold_u8(Imterface<uint8> *im_in, Imterface<uint8> *im_out, uint8 threshold)
{

    if (typeCheck(*im_in) && typeCheck(*im_out))
    {
        for (int y = 0; y < im_in->height; y++)
        {
            for (int x = 0; x < im_in->width; x++)
            {
                im_out->data[x * im_out->xStride + y * im_out->yStride] =
                        static_cast<uint8>(im_in->data[x * im_in->xStride + y * im_in->yStride] > threshold);
            }
        }
    }
    else
    {
        std::cerr << "Wrong image data type!" << std::endl;
    }
}

DLL_EXPORT float32 im_max_f(Imterface<float32> *im_in)
{
    float32 maxVal = im_in->data[0];
    if (typeCheck(*im_in))
    {
        for (int y = 0; y < im_in->height; y++)
        {
            for (int x = 0; x < im_in->width; x++)
            {
                float32 curVal = im_in->data[x * im_in->xStride + y * im_in->yStride];
                if (maxVal < curVal)
                {
                    maxVal = curVal;
                }
            }
        }
    }
    else
    {
        std::cerr << "Wrong image data type!" << std::endl;
    }
    return maxVal;
}

