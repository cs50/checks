from check50 import *


class Calc(Checks):

    @check()
    def exists(self):
        """calc.c exists"""
        self.require("calc.c")

    @check("exists")
    def compiles(self):
        """calc.c compiles"""
        self.spawn("clang -o calc calc.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test_handles_addition(self):
        """calculator handles addition"""
        self.spawn("./calc 3 + 4").stdout(number("7.000000"), "7.000000\n").exit(0)

    @check("compiles")
    def test_handles_subtraction(self):
        """calculator handles subtraction"""
        self.spawn("./calc 10.5 - 6.2").stdout(number("4.300000"), "4.300000\n").exit(0)

    @check("compiles")
    def test_handles_division(self):
        """calculator handles division"""
        self.spawn("./calc 41.48 / -8.44").stdout(number(-4.914692), "-4.914692\n").exit(0)

    @check("compiles")
    def test_handles_multiplication_with_x(self):
        """calculator handles multiplication with "x" """
        self.spawn("./calc 11.1 x 9").stdout(number(99.900002),"99.900002\n").exit(0)

    @check("compiles")
    def test_handles_modulo(self):
        """calculator handles modulo of integers"""
        self.spawn("./calc 8 % 5").stdout(number("3.000000"), "3.000000\n").exit(0)

    @check("compiles")
    def test_handles_modulo2(self):
        """calculator handles modulo of real numbers"""
        self.spawn("./calc 8.1 % 4.9").stdout(number("3.200000"), "3.200000\n").exit(0)

    @check("compiles")
    def test_handles_bad_operation(self):
        """handles invalid operation"""
        self.spawn("./calc 11 J 8").exit(1)

    @check("compiles")
    def test_argc_1(self):
        """handles lack of command line arguments"""
        self.spawn("./calc").exit(1)

    @check("compiles")
    def test_argc_5(self):
        """handles too many command line arguments"""
        self.spawn("./calc 11.1 + 23 9").exit(1)


def number(num):
    return "(^|[^\d]){}[^\d]".format(num)
