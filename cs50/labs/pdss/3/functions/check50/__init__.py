from check50 import *

class Functions(Checks):

    @check()
    def exists(self):
        """print.py submitted"""
        self.require("print.py")

    @check("exists")
    def prints_something(self):
        """prints output"""
        res = self.spawn("python3 print.py").stdout()
        if res.strip() == "":
            raise Error("no output found")

    @check("prints_something")
    def doesnt_print_hello(self):
        """prints something other than hello, world"""
        res = self.spawn("python3 print.py").stdout()
        if res.strip() == "hello, world":
            raise Error("printed hello world")

