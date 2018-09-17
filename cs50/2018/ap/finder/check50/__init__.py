from check50 import *


class Finder(Checks):

    @check()
    def exists(self):
        """finder.c exists"""
        self.require("finder.c")

    @check("exists")
    def compiles(self):
        """finder.c compiles"""
        self.spawn("clang -std=c11 -o finder finder.c -lcs50 -lm").exit(0)

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
        self.add("foo", "bar", "this", "cats.txt", "dogs.txt", "001.txt")
        self.spawn("./finder cats").exit()
        if not self.diff("001.txt", "found.txt"):
            raise Error("did not find all instances of cats")

    @check("compiles")
    def test_foo1(self):
        """finds foo with argc == 2"""
        self.add("foo", "bar", "this", "cats.txt", "dogs.txt", "002.txt")
        self.spawn("./finder foo").exit()
        if not self.diff("002.txt", "found.txt"):
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_foo2(self):
        """finds foo with argc == 3"""
        self.add("foo", "bar", "this", "cats.txt", "dogs.txt", "003.txt")
        self.spawn("./finder foo ./").exit()
        if not self.diff("003.txt", "found.txt"):
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_foo3(self):
        """finds foo in foo/"""
        self.add("foo", "bar", "this", "cats.txt", "dogs.txt", "004.txt")
        self.spawn("./finder foo foo/").exit()
        if not self.diff("004.txt", "found.txt"):
            raise Error("did not find all instances of foo")

    @check("compiles")
    def test_common(self):
        """finds common starting at ./"""
        self.add("foo", "bar", "this", "cats.txt", "dogs.txt", "005.txt")
        self.spawn("./finder common").exit()
        if not self.diff("005.txt", "found.txt"):
            raise Error("did not find all instances of common")
