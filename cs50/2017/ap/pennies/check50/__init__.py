from check50 import *


class Pennies(Checks):

    @check()
    def exists(self):
        """pennies.c exists"""
        self.require("pennies.c")

    @check("exists")
    def compiles(self):
        """pennies.c compiles"""
        self.spawn("clang -o pennies pennies.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test28days1penny(self):
        """28 days, 1 penny on day one yields $2684354.55"""
        self.spawn("./pennies").stdin("28").stdin("1").stdout("\$2684354.55\n", "$2684354.55\n").exit(0)

    @check("compiles")
    def test31days1penny(self):
        """31 days, 1 penny on day one yields $21474836.47"""
        self.spawn("./pennies").stdin("31").stdin("1").stdout("\$21474836.47\n", "$21474836.47\n").exit(0)

    @check("compiles")
    def test29days2pennies(self):
        """29 days, 2 pennies on day one yields $10737418.22"""
        self.spawn("./pennies").stdin("29").stdin("2").stdout("\$10737418.22\n", "$10737418.22\n").exit(0)

    @check("compiles")
    def test30days30pennies(self):
        """30 days, 30 pennies on day one yields $322122546.90"""
        self.spawn("./pennies").stdin("30").stdin("30").stdout("\$322122546.90\n", "$322122546.90\n").exit(0)

    @check("compiles")
    def test_invalid_days(self):
        """rejects days < 28 or > 31"""
        self.spawn("./pennies").stdin("-8").reject().stdin("35").reject().stdin("1").reject()

    @check("compiles")
    def test_negative_pennies(self):
        """rejects pennies < 1"""
        self.spawn("./pennies").stdin("31").stdin("-10").reject().stdin("0").reject()

    @check("compiles")
    def test_reject_foo_days(self):
        """rejects days == "foo" """
        self.spawn("./pennies").stdin("foo").reject()

    @check("compiles")
    def test_reject_foo_pennies(self):
        """rejects pennies == "foo" """
        self.spawn("./pennies").stdin("30").stdin("foo").reject()

    @check("compiles")
    def test_reject_empty_string_days(self):
        """rejects a non-numeric input of "" for days """
        self.spawn("./pennies").stdin("").reject()

    @check("compiles")
    def test_reject_empty_string_pennies(self):
        """rejects a non-numeric input of "" for pennies """
        self.spawn("./pennies").stdin("30").stdin("").reject()
