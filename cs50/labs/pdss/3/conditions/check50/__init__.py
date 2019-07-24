from check50 import *

class Conditions(Checks):


    @check()
    def exists(self):
        """mario.py exists."""
        self.require("mario.py")

    @check("exists")
    def test_reject_negative(self):
        """rejects a height of -1"""
        self.spawn("python3 mario.py").stdin("-1").reject()

    @check("exists")
    def test_reject_zero(self):
        """rejects a height of 0"""
        self.spawn("python3 mario.py").stdin("0").reject()

    @check("exists")
    def test_reject_5(self):
        """rejects a height of 5"""
        self.spawn("python3 mario.py").stdin("5").reject()

    @check("exists")
    def test_reject_large(self):
        """rejects a height of 28"""
        self.spawn("python3 mario.py").stdin("28").reject()

    @check("exists")
    def test1(self):
        """handles a height of 1 correctly"""
        out = self.spawn("python3 mario.py").stdin("1").stdout("^#\n$", "#\n")

    @check("exists")
    def test2(self):
        """handles a height of 2 correctly"""
        out = self.spawn("python3 mario.py").stdin("2").stdout("^#\n#\n$", "#\n#\n")

    @check("exists")
    def test4(self):
        """handles a height of 4 correctly"""
        out = self.spawn("python3 mario.py").stdin("4").stdout("^#\n#\n#\n#\n$", "#\n#\n#\n#\n")

