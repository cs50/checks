from check50 import *


class Hello(Checks):

    @check()
    def exists(self):
        """hello.c exists"""
        self.require("hello.c"), self.require("hello.c")

    @check("exists")
    def compiles(self):
        """hello.c compiles"""
        self.spawn("clang -std=c11 -o hello hello.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test_hello_world(self):
        """prints "Hello, world!" if argv[1] is "world" """
        self.spawn("./hello world").stdout("Hello, world!\n").exit(0)

    @check("compiles")
    def test_hello_elphie(self):
        """prints "Hello, elphie!" if argv[1] is "elphie" """
        self.spawn("./hello elphie").stdout("Hello, elphie!\n").exit(0)

    @check("compiles")
    def test_lack_of_arguments(self):
        """handles lack of command line arguments"""
        self.spawn("./hello").exit(1)

    @check("compiles")
    def test_too_many_arguments(self):
        """handles too many command line arguments"""
        self.spawn("./hello milo mochi elphie").exit(1)
