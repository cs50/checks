less = __import__("check50").import_from("../../less")
from less import *

class ResizeMore(ResizeLess):

    @check("compiles")
    def scale_6_to_3(self):
        """resizes 6x6-pixel BMP to 3x3 correctly when f is 0.5"""
        self.add("6x6.bmp")
        self.spawn("./resize 0.5 6x6.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["3x3.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_12_to_6(self):
        """resizes 12x12-pixel BMP to 6x6 correctly when f is 0.5"""
        self.add("12x12.bmp")
        self.spawn("./resize 0.5 12x12.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["6x6.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_18_to_9(self):
        """resizes 18x18-pixel BMP to 9x9 correctly when f is 0.5"""
        self.add("18x18.bmp")
        self.spawn("./resize 0.5 18x18.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["9x9.bmp"]:
            raise Error("resized image does not match expected image")

