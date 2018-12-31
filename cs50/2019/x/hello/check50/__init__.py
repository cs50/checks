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
        self.spawn("clang -std=c11 -o hello hello.c -lcs50 -lm").exit(0)

    @check("compiles")
    def david(self):
        """responds to name Veronica."""
        self.spawn("./hello").stdin("Veronica").stdout("Veronica", "Veronica")

    @check("compiles")
    def brian(self):
        """responds to name Brian."""
        self.spawn("./hello").stdin("Brian").stdout("Brian", "Brian")
