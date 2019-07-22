from check50 import *


class Credit(Checks):

    @check()
    def exists(self):
        """credit.c exists."""
        self.require("credit.c")

    @check("exists")
    def compiles(self):
        """credit.c compiles."""
        self.spawn("clang -std=c11 -o credit credit.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test1(self):
        """identifies 378282246310005 as AMEX"""
        self.spawn("./credit").stdin("378282246310005").stdout("^AMEX\n", "AMEX\n").exit(0)

    @check("compiles")
    def test2(self):
        """identifies 371449635398431 as AMEX"""
        self.spawn("./credit").stdin("371449635398431").stdout("^AMEX\n", "AMEX\n").exit(0)

    @check("compiles")
    def test3(self):
        """identifies 5555555555554444 as MASTERCARD"""
        self.spawn("./credit").stdin("5555555555554444").stdout("^MASTERCARD\n", "MASTERCARD\n").exit(0)

    @check("compiles")
    def test4(self):
        """identifies 5105105105105100 as MASTERCARD"""
        self.spawn("./credit").stdin("5105105105105100").stdout("^MASTERCARD\n", "MASTERCARD\n").exit(0)

    @check("compiles")
    def test5(self):
        """identifies 4111111111111111 as VISA"""
        self.spawn("./credit").stdin("4111111111111111").stdout("^VISA\n", "VISA\n").exit(0)

    @check("compiles")
    def test6(self):
        """identifies 4012888888881881 as VISA"""
        self.spawn("./credit").stdin("4012888888881881").stdout("^VISA\n", "VISA\n").exit(0)

    @check("compiles")
    def test7(self):
        """identifies 1234567890 as INVALID"""
        self.spawn("./credit").stdin("1234567890").stdout("^INVALID\n", "INVALID\n").exit(0)

    @check("compiles")
    def test8(self):
        """identifies 369421438430814 as INVALID"""
        self.spawn("./credit").stdin("369421438430814").stdout("^INVALID\n", "INVALID\n").exit(0)

    @check("compiles")
    def test9(self):
        """identifies 4062901840 as INVALID"""
        self.spawn("./credit").stdin("4062901840").stdout("^INVALID\n", "INVALID\n").exit(0)

    @check("compiles")
    def test10(self):
        """identifies 5673598276138003 as INVALID"""
        self.spawn("./credit").stdin("5673598276138003").stdout("^INVALID\n", "INVALID\n").exit(0)

    @check("compiles")
    def test11(self):
        """identifies 4111111111111113 as INVALID"""
        self.spawn("./credit").stdin("4111111111111113").stdout("^INVALID\n", "INVALID\n").exit(0)

