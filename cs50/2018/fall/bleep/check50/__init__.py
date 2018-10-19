from check50 import *


class Bleep(Checks):


    @check()
    def exists(self):
        """bleep exists"""
        self.require("bleep.py")
        self.add("banned.txt")
        self.add("banned2.txt")

    @check("exists")
    def test_reject_no_args(self):
        """rejects len(sys.argv) less than 2"""
        self.spawn("python bleep.py").exit(1)

    @check("exists")
    def test_reject_many_args(self):
        """rejects len(sys.argv) more than 2"""
        self.spawn("python bleep.py banned.txt banned.txt").exit(1)

    @check("exists")
    def test_no_banned_words(self):
        """input of 'hello world' outputs 'hello world'"""
        self.spawn("python bleep.py banned.txt").stdin("Hello world").stdout("Hello world\s*\n").exit(0)

    @check("exists")
    def test_darn(self):
        """input of 'This darn world' outputs 'This **** world'"""
        self.spawn("python bleep.py banned.txt").stdin("This darn world").stdout("This \*\*\*\* world\s*\n").exit(0)

    @check("exists")
    def handles_capitalized(self):
        """input of 'THIS DARN WORLD' outputs 'THIS **** WORLD'"""
        self.spawn("python bleep.py banned.txt").stdin("THIS DARN WORLD").stdout("THIS \*\*\*\* WORLD\s*\n").exit(0)

    @check("exists")
    def substrings(self):
        """doesn't censor substrings"""
        self.spawn("python bleep.py banned.txt").stdin("Darning my socks").stdout("Darning my socks\s*\n").exit(0)

    @check("exists")
    def handles_other_wordlists(self):
        """handles banned words lists with arbitrary words in them"""
        self.spawn("python bleep.py banned2.txt").stdin("My cat and dog are great").stdout("My \*\*\* and \*\*\* are great\s*\n").exit(0)
