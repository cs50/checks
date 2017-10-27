from check50 import *


class Scramble(Checks):

    @check()
    def exists(self):
        """scramble.c exists."""
        self.require("scramble.c")
        self.add("words.txt")

    @check("exists")
    def compiles(self):
        """scramble.c compiles."""
        (self.spawn("clang -std=c11 -o scramble scramble.c -lcs50 -lm").exit()

    @check("compiles")
    def draw3(self):
        """draws board #3 correctly"""
        self.spawn("./scramble 3").stdout("\s*N\s*E\s*H\s*I\n\s*E\s*D\s*N\s*T\n\s*T\s*E\s*A\s*I\n\s*E\s*O\s*V\s*T","  N E H I\n  E D N T\n  T E A I\n  E O V T").stdout(">")

    @check("compiles")
    def draw5(self):
        """draws board #5 correctly"""
        self.spawn("./scramble 5").stdout("\s*E\s*A\s*Y\s*A\n\s*D\s*A\s*E\s*I\n\s*L\s*T\s*A\s*E\n\s*W\s*E\s*I\s*E", "  E A Y A\n  D A E I\n  L T A E\n  W E I E").stdout(">")

    @check("compiles")
    def lookup10(self):
        """user can only score a word once"""
        self.spawn("./scramble 10").stdin("line").stdout("Score: 4").stdin("line").stdout("Score: 4").stdout("Time: .*\n\n>")

    @check("compiles")
    def lookup15(self):
        """checks if user entries exist in words.txt"""
        self.spawn("./scramble 15").stdin("hhh").stdout("Score: 0").stdin("leh").stdout("Score: 0").stdout("Time: .*\n\n>")

    @check("compiles")
    def scramble5(self):
        """scrambles board #5 correctly"""
        self.spawn("./scramble 5").stdin("scramble").stdout("\s*W\s*L\s*D\s*E\n\s*E\s*T\s*A\s*A\n\s*I\s*A\s*E\s*Y\n\s*E\s*E\s*I\s*A", "  W L D E\n  E T A A\n  I A E Y\n  E E I A")

    @check("compiles")
    def scramble7(self):
        """scrambles board #7 correctly"""
        self.spawn("./scramble 7").stdin("scramble").stdout("\s*S\s*N\s*A\s*L\n\s*S\s*A\s*L\s*T\n\s*T\s*M\s*Y\s*N\n\s*D\s*B\s*A\s*E", "  S N A L\n  S A L T\n  T M Y N\n  D B A E")
