from native_library_wrapper import NativeLibraryWrapper

pycinterface_native_lib = NativeLibraryWrapper('.', 'pycinterface')
def threshold_u8(im_in, im_out, threshold):
    return pycinterface_native_lib.threshold_u8(im_in, im_out, threshold)
def add_f(im_in1, im_in2, im_out):
    return pycinterface_native_lib.add_f(im_in1, im_in2, im_out)

