from check50 import *


class Pennies(Checks):

    @check()
    def exists(self):
        """pennies.c exist"""
        self.require("pennies.c")

    @check("exists")
    def compiles(self):
        """pennies.c compiles"""
        self.spawn("clang -std=c11 -o pennies pennies.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test28days1penny(self):
        """28 days, 1 penny on day one yields $2684354.55 """
        self.spawn("./pennies 28 1").stdout("\$2684354.55\n", "$2684354.55\n").exit(0)

    @check("compiles")
    def test29days2pennies(self):
        """29 days, 2 pennies on day one yields $10737418.22"""
        self.spawn("./pennies 29 2").stdout("\$10737418.22\n", "$10737418.22\n").exit(0)

    @check("compiles")
    def test30days30pennies(self):
        """30 days, 30 pennies on day one yields $322122546.90"""
        self.spawn("./pennies 30 30").stdout("\$322122546.90\n", "$322122546.90\n").exit(0)

    @check("compiles")
    def test31days1penny(self):
        """31 days, 1 penny on day one yields $21474836.47"""
        self.spawn("./pennies 31 1").stdout("\$21474836.47\n", "$21474836.47\n").exit(0)

    @check("compiles")
    def test_rejects_invalid_days(self):
        """rejects days < 28 or > 31"""
        self.spawn("./pennies 25 1").exit(1)

    @check("compiles")
    def test_rejects_invalid_pennies(self):
        """rejects pennies < 1"""
        self.spawn("./pennies 30 -10").exit(1)

    @check("compiles")
    def test_lack_of_arguments(self):
        """handles lack of command line arguments"""
        self.spawn("./pennies").exit(1)

    @check("compiles")
    def test_too_many_arguments(self):
        """handles too many command line arguments"""
        self.spawn("./pennies 28 35 42").exit(1)
