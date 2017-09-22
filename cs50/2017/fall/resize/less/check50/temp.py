from ctypes import *

class BitmapFile(Structure):
    _pack_ = 1
    _fields_ = [('bfType', c_uint16),
                ('bfSize', c_uint32),
                ('bfReserved1', c_uint16),
                ('bfReserved2', c_uint16),
                ('bfOffBits', c_uint32),
                ('biSize', c_uint32),
                ('biWidth', c_int32),
                ('biHeight', c_int32),
                ('biPlanes', c_uint16),
                ('biBitCount', c_uint16),
                ('biCompression', c_uint32),
                ('biSizeImage', c_uint32),
                ('biXPelsPerMeter', c_int32),
                ('biYPelsPerMeter', c_int32),
                ('biClrUsed', c_uint32),
                ('biClrImportant', c_uint32)]

with open("test.bmp", "rb") as f:
    x = BitmapFile()
    f.readinto(x)
    for field, _ in BitmapFile._fields_:
        print("{}: {}".format(field, hex(getattr(x, field))))

with open("test.bmp", "rb") as f:
    f.seek(54, 0)
    x = f.read(1)
    print(x)
