from check50 import *


class Bleep(Checks):


    @check()
    def exists(self):
        """bleep exists."""
        self.require("bleep")
        self.add("banned.txt")

    @check("exists")
    def test_reject_no_args(self):
        """rejects len(sys.argv) less than 2"""
        self.spawn("./bleep").exit(1)

    @check("exists")
    def test_reject_many_args(self):
        """rejects len(sys.argv) more than 2"""
        self.spawn("./bleep banned.txt banned.txt").exit(1)

    @check("exists")
    def test_no_banned_words(self):
        """leaves phrases with no banned words alone"""
        self.spawn("./bleep banned.txt").stdin("Hello world").stdout("Hello world\n").exit(0)

    @check("exists")
    def test_darn(self):
        """input of 'This darn world' outputs 'This **** world'"""
        self.spawn("./bleep banned.txt").stdin("This darn world").stdout("This [*][*][*][*] world\n").exit(0)

    @check("exists")
    def handles_capitalizing(self):
        """input of 'THIS DARN WORLD' outputs 'THIS **** WORLD'"""
        self.spawn("./bleep banned.txt").stdin("THIS DARN WORLD").stdout("THIS [*][*][*][*] WORLD\n").exit(0)
