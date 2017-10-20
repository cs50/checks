import re

from check50 import *

class Hello(Checks):

    @check()
    def exists(self):
        """hello.py exists."""
        self.require("hello.py")

    @check("exists")
    def prints_hello(self):
        """prints "hello, world\\n" """
        expected = "[Hh]ello, world!?\n"
        actual = self.spawn("python hello.py").stdout()
        if not re.match(expected, actual):
            err = Error(Mismatch("hello, world\n", actual))
            if re.match(expected[:-1], actual):
                err.helpers = "Did you forget a newline (\"\\n\") at the end of your string?"
            raise err
