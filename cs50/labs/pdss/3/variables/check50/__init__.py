from check50 import *
import os


class Input(Checks):

    @check()
    def exists(self):
        """input.py submitted"""
        self.require("input.py")

    @check("exists")
    def david(self):
        """responds to name David"""
        self.spawn("python input.py").stdin("David").stdout("hello, David", "hello, David")

    @check("exists")
    def maria(self):
        """responds to name Maria"""
        self.spawn("python input.py").stdin("Maria").stdout("hello, Maria", "hello, Maria")
