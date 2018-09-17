from check50 import *


class FindLess(Checks):

    @check()
    def exists(self):
        """helpers.c exists."""
        self.require("helpers.c")

    @check("exists")
    def compiles(self):
        """helpers.c compiles."""
        self.add("helpers.h")
        self.add("find.c")
        self.add("sort.c")
        self.spawn("clang -std=c11 -o sort sort.c helpers.c -lcs50 -lm").exit(0)
        self.spawn("clang -std=c11 -o find find.c helpers.c -lcs50 -lm").exit(0)

    def test_sorted(self, items):
        p = self.spawn("./sort")
        for i in items:
            p.stdin(str(i))
        p.stdin(EOF)
        for i in sorted(items):
            p.stdout(str(i))
        p.exit(0)

    @check("compiles")
    def sort_reversed(self):
        """sorts {5,4,3,2,1}"""
        self.test_sorted([5, 4, 3, 2, 1])

    @check("compiles")
    def sort_shuffled(self):
        """sorts {5,3,1,2,4,6}"""
        self.test_sorted([5, 3, 1, 2, 4, 6])

    @check("compiles")
    def first_among_three(self):
        """finds 28 in {28,29,30}"""
        self.spawn("./find 28").stdin("28").stdin("29").stdin("30").stdin(EOF).exit(0)

    @check("compiles")
    def second_among_three(self):
        """finds 28 in {27,28,29}"""
        self.spawn("./find 28").stdin("27").stdin("28").stdin("29").stdin(EOF).exit(0)

    @check("compiles")
    def third_among_three(self):
        """finds 28 in {26,27,28}"""
        self.spawn("./find 28").stdin("26").stdin("27").stdin("28").stdin(EOF).exit(0)

    @check("compiles")
    def second_among_four(self):
        """finds 28 in {27,28,29,30}"""
        self.spawn("./find 28").stdin("27").stdin("28").stdin("29").stdin("30").stdin(EOF).exit(0)

    @check("compiles")
    def third_among_four(self):
        """finds 28 in {26,27,28,29}"""
        self.spawn("./find 28").stdin("26").stdin("27").stdin("28").stdin("29").stdin(EOF).exit(0)

    @check("compiles")
    def fourth_among_four(self):
        """finds 28 in {25,26,27,28}"""
        self.spawn("./find 28").stdin("25").stdin("26").stdin("27").stdin("28").stdin(EOF).exit(0)

    @check("compiles")
    def not_among_three(self):
        """doesn't find 28 in {25,26,27}"""
        self.spawn("./find 28").stdin("25").stdin("26").stdin("27").stdin(EOF).exit(1)

    @check("compiles")
    def not_among_four(self):
        """doesn't find 28 in {25,26,27,29}"""
        self.spawn("./find 28").stdin("25").stdin("26").stdin("27").stdin("29").stdin(EOF).exit(1)

    @check("compiles")
    def needle_too_low_four(self):
        """doesn't find 28 in {29,30,31,32}"""
        self.spawn("./find 28").stdin("29").stdin("30").stdin("31").stdin("32").stdin(EOF).exit(1)

    @check("compiles")
    def needle_too_low_three(self):
        """doesn't find 28 in {29, 30, 31}"""
        self.spawn("./find 28").stdin("29").stdin("30").stdin("31").stdin(EOF).exit(1)

    @check("compiles")
    def correctly_sorts(self):
        """finds 28 in {30,27,28,26}"""
        self.spawn("./find 28").stdin("30").stdin("27").stdin("28").stdin("26").stdin(EOF).exit(0)
