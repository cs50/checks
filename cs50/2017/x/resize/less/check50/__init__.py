from check50 import *


class ResizeLess(Checks):
    hashes = {
        "3x3.bmp": "7762f5ed1684a1fb02d8dfd8e6fc248c00b8326d1d3c27df7a1c6a4f5ac278be",
        "6x6.bmp": "671254daeafeef77b9ce02819bea34f2e63d9e0ab6932c0b896adb2c24dc003e",
        "9x9.bmp": "8fedc60697f4a001cb489621d03051e8639f0a7ec6f0ec3b61014edb3271eacb",
        "12x12.bmp": "959b7760fd4fe12f29b4413c97ed7be33440caeb3253503b05b44dcd0afa641b",
        "15x15.bmp": "324931798c0de09c29957d790e0ef800a02a42274a5b147451137c042611bcd7",
        "18x18.bmp": "783123e79d8142b6d25518d6d43223d338f7aada6da9ecfd4bd29417d7b14e1e"
    }

    @check()
    def exists(self):
        """resize.c and bmp.h exist."""
        self.add("bmp.h")
        self.require("resize.c")

    @check("exists")
    def compiles(self):
        """resize.c compiles."""
        self.spawn("clang -o resize resize.c -lm -lcs50").exit(0)

    @check("compiles")
    def scale_by_1(self):
        """doesn't resize 3x3-pixel BMP when n is 1"""
        self.add("3x3.bmp")
        self.spawn("./resize 1 3x3.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["3x3.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_by_2(self):
        """resizes 3x3-pixel BMP to 6x6 correctly when n is 2"""
        self.add("3x3.bmp")
        self.spawn("./resize 2 3x3.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["6x6.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_by_3(self):
        """resizes 3x3-pixel BMP to 9x9 correctly when n is 3"""
        self.add("3x3.bmp")
        self.spawn("./resize 3 3x3.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["9x9.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_by_4(self):
        """resizes 3x3-pixel BMP to 12x12 correctly when n is 4"""
        self.add("3x3.bmp")
        self.spawn("./resize 4 3x3.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["12x12.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_by_5(self):
        """resizes 3x3-pixel BMP to 15x15 correctly when n is 5"""
        self.add("3x3.bmp")
        self.spawn("./resize 5 3x3.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["15x15.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_6_to_12(self):
        """resizes 6x6-pixel BMP to 12x12 correctly when n is 2"""
        self.add("6x6.bmp")
        self.spawn("./resize 2 6x6.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["12x12.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_9_to_18(self):
        """resizes 9x9-pixel BMP to 18x18 correctly when n is 2"""
        self.add("9x9.bmp")
        self.spawn("./resize 2 9x9.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["18x18.bmp"]:
            raise Error("resized image does not match expected image")

    @check("compiles")
    def scale_6_to_18(self):
        """resizes 6x6-pixel BMP to 18x18 correctly when n is 3"""
        self.add("6x6.bmp")
        self.spawn("./resize 3 6x6.bmp outfile.bmp").exit(0)
        if self.hash("outfile.bmp") != self.hashes["18x18.bmp"]:
            raise Error("resized image does not match expected image")
