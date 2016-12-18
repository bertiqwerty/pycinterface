# coding: utf-8
"""
@author behrang
@file
@date Oct 13, 2016
@details Demo of the native libraries with c-style interface
"""

import numpy as np
import ctypes
import native
import sys

def scale_2_01(im_in):
    tmp = np.amin(im_in)
    im_scaled = im_in - tmp
    tmp = float(np.amax(im_scaled))
    im_scaled /= tmp
    return im_scaled


def create_compare_with_ref_str(name, x, ref):
    print("start comp")
    diff = np.sum(np.abs(x - ref))
    print("diff is %s" % diff)
    print(sys.getrefcount(x))
    return name + ": " + ("OK" if diff < 1e-6 else "FAILED")

if __name__ == "__main__":

    # Threshold example with numpy views
    im = (scale_2_01(np.random.randn(100, 100)) * 255).astype(np.uint8)
    im_out = np.zeros_like(im)
    native.threshold_u8(im[11:20, 11:20], im_out[21:30, 11:20], 127)
    print(create_compare_with_ref_str("threshold", im_out[21:30, 11:20], im[11:20, 11:20] > 127))

    # maximum value of array
    print(create_compare_with_ref_str("amax", np.amax(im), native.im_max_f(im.astype(np.float32))))


    # Addition example
    for i in range(1):
        im1 = np.random.randn(500, 500).astype(np.float32)
        im2 = np.random.randn(500, 500).astype(np.float32)
        # im_out = im1 + im2
        im_out = native.add_f(im1, im2)
    print(im_out.shape)
    #print(create_compare_with_ref_str("addition", im_out, im1 + im2))
    print("done")

    # # Typecheck fails
    # im1 = np.random.randn(10, 10).astype(np.uint8)
    # im2 = np.random.randn(10, 10).astype(np.float32)
    # im_out = np.zeros_like(im1)
    # native.add_f(im1, im2, im_out)
    # print(create_compare_with_ref_str("invalid type", im_out, np.zeros_like(im1)))
    #
