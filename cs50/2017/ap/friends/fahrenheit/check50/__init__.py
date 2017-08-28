from check50 import *


class Fahrenheit(Checks):

    @check()
    def exists(self):
        """fahrenheit.c exists"""
        self.require("fahrenheit.c")

    @check("exists")
    def compiles(self):
        """fahrenheit.c compiles"""
        self.spawn("clang -o fahrenheit fahrenheit.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test37(self):
        """37 degrees Celsius yields 98.6 degrees Fahrenheit"""
        self.spawn("./fahrenheit 37").stdout(number(98.6), "98.6\n").exit(0)

    @check("compiles")
    def test0(self):
        """0 degrees Celsius yields 32.0 degrees Fahrenheit"""
        self.spawn("./fahrenheit 0").stdout(number(32.0), "32.0\n").exit(0)

    @check("compiles")
    def test100point00(self):
        """100.00 degrees Celsius yields 212.0 degrees Fahrenheit"""
        self.spawn("./fahrenheit 100.00").stdout(number(212.0), "212.0\n").exit(0)

    @check("compiles")
    def testneg40(self):
        """-40 degrees Celsius yields -40.0 degrees Fahrenheit"""
        self.spawn("./fahrenheit -40").stdout(number(-40.0), "-40.0\n").exit(0)

    @check("compiles")
    def test_lack_of_arguments(self):
        """handles lack of command line arguments"""
        self.spawn("./fahrenheit").exit(1)

    @check("compiles")
    def test_too_many_arguments(self):
        """handles too many command line arguments"""
        self.spawn("./fahrenheit 0 32").exit(1)


def number(num):
    return "(^|[^\d]){}[^\d]".format(num)
