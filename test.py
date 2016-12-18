import numpy as np
import numpy.linalg as la
import native
from native_library_wrapper import NdCustomDeleteArray
if __name__ == '__main__':
    y = np.ones((10, 10), dtype=np.float32)
    def tmp():
        y = np.ones((10, 10), dtype=np.float32)

        x = NdCustomDeleteArray(np.ones((10,10), dtype=np.float32))
    #    print(x[1:2,3:5]+y[1:2,3:5])
    #    print(type(x[1:2,3:5]))
        #return x + y
    #z = tmp()
    #print(type(z.data))

    im_out = native.add_f(y, y)


    print(im_out.ndarray)

    im_out.__del__()