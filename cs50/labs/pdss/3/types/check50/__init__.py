from check50 import *
import os


class Types(Checks):

    @check()
    def exists(self):
        """types.py submitted"""
        self.require("types.py")

    @check("exists")
    def positives(self):
        """computes 1 + 1 as 2"""
        self.spawn("python3 types.py").stdin("1").stdin("1").stdout("2", "2")

    @check("exists")
    def zero(self):
        """computes 5 + 0 as 5"""
        self.spawn("python3 types.py").stdin("5").stdin("0").stdout("5", "5")

    @check("exists")
    def negative(self):
        """computes -10 + 38 as 28"""
        self.spawn("python3 types.py").stdin("-10").stdin("38").stdout("28", "28")
