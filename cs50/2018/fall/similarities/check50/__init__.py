import imp

from contextlib import redirect_stdout
from check50 import *

class Similarities(Checks):

    @check()
    def exists(self):
        """helpers.py exists"""
        self.require("helpers.py")

    @check("exists")
    def compiles(self):
        """helpers.py compiles"""
        try:
            helpers = imp.load_source("helpers", "helpers.py")
        except Exception as e:
            raise Error(str(e))

    def check_strings(self, method, a, b, expected, length=1):
        try:
            helpers = imp.load_source("helpers", "helpers.py")
            self.log.append("Running {} on inputs {} and {}...".format(method, repr(a), repr(b)))
            with open("/dev/null", "w") as f:
                with redirect_stdout(f):
                    if method != "substrings":
                        actual = getattr(helpers, method)(a, b)
                    else:
                        actual = getattr(helpers, method)(a, b, length)
            if len(actual) != len(expected):
                raise Error("Expected {} matches, not {}".format(len(expected), len(actual)))
            actual = set(actual)
            if actual != expected:
                raise Error("Expected {}, not {}".format(expected or "{}", actual or "{}"))
        except Error as e:
            raise e
        except Exception as e:
            raise Error(str(e))

    @check("compiles")
    def lines_none(self):
        """detects no lines in common"""
        a = "Line 1\nLine 2"
        b = "Line 3\nLine 4"
        expected = set()
        self.check_strings("lines", a, b, expected)

    @check("compiles")
    def lines_one(self):
        """detects one line in common"""
        a = "Line 1\nLine 2\nLine 3\nLine 4"
        b = "Line 5\nLine 6\nLine 3\nLine 8"
        expected = {"Line 3"}
        self.check_strings("lines", a, b, expected)

    @check("compiles")
    def lines_multiple(self):
        """detects multiple lines in common"""
        a = "Line 1\nLine 2\nLine 3\nLine 4"
        b = "Line 4\nLine 6\nLine 3\nLine 8"
        expected = {"Line 3", "Line 4"}
        self.check_strings("lines", a, b, expected)

    @check("compiles")
    def lines_duplicates(self):
        """handles duplicate lines in common"""
        a = "Line 1\nLine 2\nLine 3\nLine 4"
        b = "Line 4\nLine 6\nLine 3\nLine 8\nLine 3"
        expected = {"Line 3", "Line 4"}
        self.check_strings("lines", a, b, expected)

    @check("compiles")
    def sentences_none(self):
        """handles no sentences in common"""
        a = "This is a sentence. Here is another one."
        b = "This is a third sentence. A fourth. A fifth."
        expected = set()
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def sentences_one(self):
        """handles one sentence in common"""
        a = "This is a sentence. Here is another one."
        b = "This is a third sentence. Here is another one. A fifth."
        expected = {"Here is another one."}
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def sentences_multiple(self):
        """handles multiple sentences in common"""
        a = "This is a sentence. Here is another one."
        b = "This is a third sentence. Here is another one. This is a sentence."
        expected = {"Here is another one.", "This is a sentence."}
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def sentences_punctuation(self):
        """handles sentences with different punctuation"""
        a = "Is this a sentence? Here is another one!"
        b = "This is a third sentence. Here is another one. Is this a sentence?"
        expected = {"Is this a sentence?"}
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def sentences_mid_punctuation(self):
        """handles sentences with punctuation mid-sentence"""
        a = "One... two... three. Four. Five."
        b = "Four. One... two... three. Six."
        expected = {"One... two... three.", "Four."}
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def sentences_duplicates(self):
        """handles duplicate sentences in common"""
        a = "This is one. This is two. This is three. This is two. This is one."
        b = "This is three. This is two. This is four. This is five."
        expected = {"This is three.", "This is two."}
        self.check_strings("sentences", a, b, expected)

    @check("compiles")
    def substrings_none(self):
        """handles no substrings in common"""
        a = "foo"
        b = "bar"
        expected = set()
        self.check_strings("substrings", a, b, expected, length=1)
        self.check_strings("substrings", a, b, expected, length=2)
        self.check_strings("substrings", a, b, expected, length=3)

    @check("compiles")
    def substrings_one(self):
        """handles one substring in common"""
        a = "foobar"
        b = "bar"
        self.check_strings("substrings", a, b, {"bar"}, length=3)

    @check("compiles")
    def substrings_multiple(self):
        """handles multiple substrings in common"""
        a = "foobar"
        b = "barfoo"
        self.check_strings("substrings", a, b, {"fo", "oo", "ba", "ar"}, length=2)
        self.check_strings("substrings", a, b, {"foo", "bar"}, length=3)

    @check("compiles")
    def substrings_identical(self):
        """handles substrings when strings are identical"""
        a = "foobar"
        b = "foobar"
        self.check_strings("substrings", a, b, {"foo", "oob", "oba","bar"}, length=3)
        self.check_strings("substrings", a, b, {"foob", "ooba", "obar"}, length=4)
        self.check_strings("substrings", a, b, {"fooba", "oobar"}, length=5)
        self.check_strings("substrings", a, b, {"foobar"}, length=6)

    @check("compiles")
    def substrings_bounds(self):
        """handles substring length longer than string length"""
        a = "foobar"
        b = "foobar"
        self.check_strings("substrings", a, b, set(), length=7)

    @check("compiles")
    def substrings_duplicates(self):
        """handles duplicate substrings in common"""
        a = "foobarbaz"
        b = "barbaz"
        self.check_strings("substrings", a, b, {"ba", "ar", "rb", "az"}, length=2)
