from check50 import *


class isbn(Checks):

    @check()
    def exists(self):
        """isbn.c exists"""
        self.require("isbn.c")

    @check("exists")
    def compiles(self):
        """isbn.c compiles"""
        self.spawn("clang -o isbn isbn.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test_Absolute_Beginners_Guide(self):
        """Beginners Guide (0789751984) valid"""
        self.spawn("./isbn").stdin("0789751984").stdout("^YES\n", "YES\n").exit(0)

    @check("compiles")
    def test_Absolute_Beginners_Guide_fake(self):
        """Beginners Guide fake (0789751985) invalid"""
        self.spawn("./isbn").stdin("0789751985").stdout("^NO\n", "NO\n").exit(0)

    @check("compiles")
    def test_Programming_in_C(self):
        """Programming in C (0321776410) valid"""
        self.spawn("./isbn").stdin("0321776410").stdout("^YES\n", "YES\n").exit(0)

    @check("compiles")
    def test_Hackers_Delight(self):
        """Hackers Delight (0321842685) valid"""
        self.spawn("./isbn").stdin("0321842685").stdout("^YES\n", "YES\n").exit(0)

    @check("compiles")
    def test_phone_number(self):
        """Jennys number (6178675309) invalid"""
        self.spawn("./isbn").stdin("6178675309").stdout("^NO\n", "NO\n").exit(0)

    @check("compiles")
    def test_memory(self):
        """Mystery Test"""
        self.spawn("./isbn").stdin("1632168146").stdout("^YES\n", "YES\n").exit(0)

    @check("compiles")
    def test_ISBN_with_X(self):
        """rejects ISBNs with X as checksum"""
        self.spawn("./isbn").stdin("078974984X").reject()

    @check("compiles")
    def test_rejects_ISBNs_with_dashes(self):
        """rejects ISBNs with dashes"""
        self.spawn("./isbn").stdin("0-789-75198-4").reject()

    @check("compiles")
    def test_reject_empty(self):
        """rejects a non-numeric input of "" """
        self.spawn("./isbn").stdin("").reject()
