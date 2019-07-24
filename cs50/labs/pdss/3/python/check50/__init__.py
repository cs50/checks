from check50 import *


class Hello(Checks):

    @check()
    def exists(self):
        """hello.py submitted"""
        self.require("hello.py")

    @check("exists")
    def hello(self):
        """says hello"""
        self.spawn("python3 hello.py").stdout("hello, world", "hello, world")
