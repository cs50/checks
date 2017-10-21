import imp

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

    def check_distance(self, a, b, expected):
        try:
            helpers = imp.load_source("helpers", "helpers.py")
            self.log.append("Checking edit distance for inputs {} and {}...".format(repr(a), repr(b)))
            actual = helpers.distances(a, b)[len(a)][len(b)][0]
            if actual != expected:
                raise Error("Expected edit distance of {}, not {}".format(expected, actual))
        except Error as e:
            raise e
        except Exception as e:
            raise Error(str(e))

    @check("compiles")
    def edit_empty(self):
        """takes 0 operation to convert "" to "" """
        self.check_distance("", "", 0)

    @check("compiles")
    def edit_from_empty(self):
        """takes 3 operation to convert "dog" to "" """
        self.check_distance("dog", "", 3)

    @check("compiles")
    def edit_to_empty(self):
        """takes 4 operation to convert "" to "dog" """
        self.check_distance("", "dog", 3)

    @check("compiles")
    def edit_a_b(self):
        """takes 1 operation to convert "a" to "b" """
        self.check_distance("a", "b", 1)

    @check("compiles")
    def edit_insertion(self):
        """takes 1 operation to convert "cat" to "coat" """
        self.check_distance("cat", "coat", 1)

    @check("compiles")
    def edit_deletion(self):
        """takes 1 operation to convert "frog" to "fog" """
        self.check_distance("frog", "fog", 1)

    @check("compiles")
    def edit_substitution(self):
        """takes 1 operation to convert "year" to "pear" """
        self.check_distance("year", "pear", 1)

    @check("compiles")
    def edit_identical(self):
        """takes 0 operations to convert "today" to "today" """
        self.check_distance("today", "today", 0)

    @check("compiles")
    def edit_to_longer(self):
        """takes 5 operations to convert "today" to "yesterday" """
        self.check_distance("today", "yesterday", 5)

    @check("compiles")
    def edit_to_shorter(self):
        """takes 6 operations to convert "tomorrow" to "today" """
        self.check_distance("tomorrow", "today", 6)

    @check("compiles")
    def edit_handles_case(self):
        """takes 3 operations to convert "today" to "ToDaY" """
        self.check_distance("today", "ToDaY", 3)
