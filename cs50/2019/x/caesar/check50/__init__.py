from check50 import *


class Caesar(Checks):

    @check()
    def exists(self):
        """caesar.c exists."""
        self.require("caesar.c")

    @check("exists")
    def compiles(self):
        """caesar.c compiles."""
        self.spawn("clang -std=c11 -o caesar caesar.c -lcs50 -lm").exit(0)

    @check("compiles")
    def encrypts_a_as_b(self):
        """encrypts "a" as "b" using 1 as key"""
        self.spawn("./caesar 1").stdin("a").stdout("[Cc]iphertext:\s*b\n", "ciphertext: b\n").exit(0)

    @check("compiles")
    def encrypts_barfoo_as_yxocll(self):
        """encrypts "barfoo" as "yxocll" using 23 as key"""
        self.spawn("./caesar 23").stdin("barfoo").stdout("[Cc]iphertext:\s*yxocll\n", "ciphertext: yxocll\n").exit(0)

    @check("compiles")
    def encrypts_BARFOO_as_EDUIRR(self):
        """encrypts "BARFOO" as "EDUIRR" using 3 as key"""
        self.spawn("./caesar 3").stdin("BARFOO").stdout("[Cc]iphertext:\s*EDUIRR\n", "ciphertext: EDUIRR\n").exit(0)

    @check("compiles")
    def encrypts_BaRFoo_FeVJss(self):
        """encrypts "BaRFoo" as "FeVJss" using 4 as key"""
        self.spawn("./caesar 4").stdin("BaRFoo").stdout("[Cc]iphertext:\s*FeVJss\n", "ciphertext: FeVJss\n").exit(0)

    @check("compiles")
    def encrypts_barfoo_as_onesbb(self):
        """encrypts "barfoo" as "onesbb" using 65 as key"""
        self.spawn("./caesar 65").stdin("barfoo").stdout("[Cc]iphertext:\s*onesbb\n", "ciphertext: onesbb\n").exit(0)

    @check("compiles")
    def checks_for_handling_non_alpha(self):
        """encrypts "world, say hello!" as "iadxp, emk tqxxa!" using 12 as key"""
        self.spawn("./caesar 12").stdin("world, say hello!").stdout("[Cc]iphertext:\s*iadxp, emk tqxxa!\n", "ciphertext: iadxp, emk tqxxa!\n").exit(0)

    @check("compiles")
    def handles_no_argv(self):
        """handles lack of argv[1]"""
        self.spawn("./caesar").exit(1)
        
    @check("compiles")
    def toomanyargs(self):
        """handles argc > 2"""
        self.spawn("./caesar 1 2 3").exit(1)
    
    @check("compiles")
    def rejects_non_numeric(self):
        """rejects non-numeric argv[1]"""
        self.spawn("./caesar 2a!").exit(1)
        
  
