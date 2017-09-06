import re

from check50 import *

class Hello(Checks):

    @check()
    def exists(self):
        """hello.c exists."""
        self.require("hello.c")

    @check("exists")
    def compiles(self):
        """hello.c compiles."""
        self.spawn("clang -o hello hello.c").exit(0)

    @check("compiles")
    def prints_hello(self):
        """prints "hello, world\\n" """
        expected = "[Hh]ello, world!?\n"
        actual = self.spawn("./hello").stdout()
        if not re.match(expected, actual):
            err = Error(Mismatch("hello, world\n", actual))
            if re.match(expected[:-1], actual):
                err.helpers = "Did you forget a newline (\"\\n\") at the end of your printf string?"
            raise err
