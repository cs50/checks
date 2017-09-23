from check50 import *
from ctypes import *

class BitmapFile(Structure):
    """Structure to maintain BITMAPFILEHEADER and BITMAPINFOHEADER"""
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

class ResizeLess(Checks):

    def check_bmps(self, expected_filename, actual_filename):
    
        # Open files.
        expected_file = open(expected_filename, "rb")
        actual_file = open(actual_filename, "rb")
        
        # Read in the headers.
        expected_header = BitmapFile()
        actual_header = BitmapFile()
        expected_file.readinto(expected_header)
        actual_file.readinto(actual_header)

        # Compare headers.
        for field, _ in BitmapFile._fields_:
            if getattr(expected_header, field) != getattr(actual_header, field):
                expected_file.close()
                actual_file.close()
                raise Error("Header field {} doesn't match. Expected {}, not {}".format(field,
                    hex(getattr(expected_header, field)), hex(getattr(actual_header, field))))
    
        byte_count = 0
        while True:
            expected_byte = expected_file.read(1)
            actual_byte = actual_file.read(1)
            if expected_byte == b'' and actual_byte == b'':
                break
            elif expected_byte == b'':
                expected_file.close()
                actual_file.close()
                raise Error("Image has more bytes than expected.")
            elif actual_byte == b'':
                expected_file.close()
                actual_file.close()
                raise Error("Image has fewer bytes than expected.")
            byte_count += 1
            if expected_byte != actual_byte:
                expected_file.close()
                actual_file.close()
                raise Error("Byte {} of pixel data doesn't match. Expected 0x{}, not 0x{}".format(
                    byte_count, expected_byte.hex(), actual_byte.hex()))
        
        # Close files.
        expected_file.close()
        actual_file.close()

    @check()
    def exists(self):
        """resize.c and bmp.h exist."""
        self.add("bmp.h")
        self.add("small.bmp", "smiley.bmp", "large.bmp")
        self.add("small2.bmp", "small3.bmp", "small4.bmp", "small5.bmp")
        self.add("large2.bmp", "smiley2.bmp", "smiley3.bmp")
        self.require("resize.c")

    @check("exists")
    def compiles(self):
        """resize.c compiles."""
        self.spawn("clang -std=c11 -o resize resize.c -lm -lcs50").exit(0)

    @check("compiles")
    def small_1(self):
        """doesn't resize small.bmp when n is 1"""
        self.spawn("./resize 1 small.bmp outfile.bmp").exit(0)
        self.check_bmps("small.bmp", "outfile.bmp")

    @check("compiles")
    def small_2(self):
        """resizes small.bmp correctly when n is 2"""
        self.spawn("./resize 2 small.bmp outfile.bmp").exit(0)
        self.check_bmps("small2.bmp", "outfile.bmp")

    @check("compiles")
    def small_3(self):
        """resizes small.bmp correctly when n is 3"""
        self.spawn("./resize 3 small.bmp outfile.bmp").exit(0)
        self.check_bmps("small3.bmp", "outfile.bmp")

    @check("compiles")
    def small_4(self):
        """resizes small.bmp correctly when n is 4"""
        self.spawn("./resize 4 small.bmp outfile.bmp").exit(0)
        self.check_bmps("small4.bmp", "outfile.bmp")

    @check("compiles")
    def small_5(self):
        """resizes small.bmp correctly when n is 5"""
        self.spawn("./resize 5 small.bmp outfile.bmp").exit(0)
        self.check_bmps("small5.bmp", "outfile.bmp")
        
    @check("compiles")
    def large_2(self):
        """resizes large.bmp correctly when n is 2"""
        self.spawn("./resize 2 large.bmp outfile.bmp").exit(0)
        self.check_bmps("large2.bmp", "outfile.bmp")

    @check("compiles")
    def smiley_2(self):
        """resizes smiley.bmp correctly when n is 2"""
        self.spawn("./resize 2 smiley.bmp outfile.bmp").exit(0)
        self.check_bmps("smiley2.bmp", "outfile.bmp")
        
    @check("compiles")
    def smiley_3(self):
        """resizes smiley.bmp correctly when n is 3"""
        self.spawn("./resize 3 smiley.bmp outfile.bmp").exit(0)
        self.check_bmps("smiley3.bmp", "outfile.bmp")
