/**
 * @author behrang
 * @file
 * @date Oct 13, 2016
 * @details Example C++ library with interface to Python
 */

#include "OsDetection.h"
#include "ImageTypes.h"
#include <iostream>



DLL_EXPORT void add_f(Imterface<float32> *im_in1, Imterface<float32> *im_in2, Imterface<float32> *im_out)
{

    // You probably don't want to use the Imterface instance directly but create an image class that checks
    // the type in its constructor and, allocate memory without using 'new', and has convenient access operators.
    if (typeCheck(*im_in1) && typeCheck(*im_in2) && typeCheck(*im_out))
    {
        for (int y = 0; y < im_in1->height; y++)
        {
            for (int x = 0; x < im_in1->width; x++)
            {
                im_out->data[x * im_out->xStride + y * im_out->yStride] =
                        im_in1->data[x * im_in1->xStride + y * im_in1->yStride] + im_in2->data[x * im_in2->xStride + y * im_in2->yStride];
            }
        }
    }
    else
    {
        std::cerr << "Wrong image data type!" << std::endl;
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


