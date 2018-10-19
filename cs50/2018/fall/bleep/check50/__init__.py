from check50 import *


class Bleep(Checks):


    @check()
    def exists(self):
        """bleep exists"""
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
        """input of 'hello world' outputs 'hello world'"""
        self.spawn("./bleep banned.txt").stdin("Hello world").stdout("Hello world\s*\n").exit(0)

    @check("exists")
    def test_darn(self):
        """input of 'This darn world' outputs 'This **** world'"""
        self.spawn("./bleep banned.txt").stdin("This darn world").stdout("This \*\*\*\* world\s*\n").exit(0)

    @check("exists")
    def handles_capitalized(self):
        """input of 'THIS DARN WORLD' outputs 'THIS **** WORLD'"""
        self.spawn("./bleep banned.txt").stdin("THIS DARN WORLD").stdout("THIS \*\*\*\* WORLD\s*\n").exit(0)

    @check("exists")
    def substrings(self):
        """doesn't censor substrings"""
        self.spawn("./bleep banned.txt").stdin("Darning my socks").stdout("Darning my socks").exit(0)

    @check("exists")
    def handles_other_wordlists(self):
        """handles banned words list with arbitrary words in them"""
        self.spawn("./bleep banned2.txt").stdin("I own a cat and a dog").stdout("I own a \*\*\* and a \*\*\*\s*\n").exit(0)
