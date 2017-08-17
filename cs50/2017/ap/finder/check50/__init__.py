from check50 import *


class Finder(Checks):

    @check()
    def exists(self):
        """finder.c exists"""
        self.require("finder.c")

    @check("exists")
    def compiles(self):
        """finder.c compiles"""
        self.spawn("clang -o finder finder.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test_handles_lack_of_arguments(self):
        """handles lack of arguments"""
        self.spawn("./finder").exit(1)

    @check("compiles")
    def test_handles_too_many_arguments(self):
        """handles too many arguments"""
        self.spawn("./finder x y z").exit(1)

    @check("compiles")
    def test_cats(self):
        """finds cats in cats.txt"""
        self.add("foo"), self.add("bar"), self.add("this"), self.add("cats.txt"), self.add("dogs.txt"), self.add("001.txt")
        self.spawn("./finder cats").exit()
        if self.diff("001.txt", "found.txt") == False:
            raise Error("did not find all instances of cats")

    @check("compiles")
    def test_foo1(self):
        """finds foo with argc == 2"""
        self.add("foo"), self.add("bar"), self.add("this"), self.add("cats.txt"), self.add("dogs.txt"), self.add("002.txt")
        self.spawn("./finder foo").exit()
        if self.diff("002.txt", "found.txt") == False:
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_foo2(self):
        """finds foo with argc == 3"""
        self.add("foo"), self.add("bar"), self.add("this"), self.add("cats.txt"), self.add("dogs.txt"), self.add("003.txt")
        self.spawn("./finder foo ./").exit()
        if self.diff("003.txt", "found.txt") == False:
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_foo3(self):
        """finds foo in foo/"""
        self.add("foo"), self.add("bar"), self.add("this"), self.add("cats.txt"), self.add("dogs.txt"),self.add("004.txt")
        self.spawn("./finder foo foo/").exit()
        if self.diff("004.txt", "found.txt") == False:
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_common(self):
        """finds common starting at ./"""
        self.add("foo"), self.add("bar"), self.add("this"), self.add("cats.txt"), self.add("dogs.txt"), self.add("005.txt")
        self.spawn("./finder common").exit()
        if self.diff("005.txt", "found.txt") == False:
            raise Error("did not find all instances of common")
