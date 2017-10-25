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
        self.spawn(self.spawn("clang -std=c11 -o scramble scramble.c -lcs50 -lm").exit())

    @check("compiles")
    def draw3(self):
        """draws board correctly"""
        self.spawn("./scramble 3").stdout("\s*N\s*E\s*H\s*I\n\s*E\s*D\s*N\s*T\n\s*T\s*E\s*A\s*I\n\s*E\s*O\s*V\s*T","  N E H I\n  E D N T\n  T E A I\n  E O V T").stdout(">")

    @check("compiles")
    def draw5(self):
        """draws board correctly"""
        self.spawn("./scramble 5").stdout("\s*E\s*A\s*Y\s*A\n\s*D\s*A\s*E\s*I\n\s*L\s*T\s*A\s*E\n\s*W\s*E\s*I\s*E", "  E A Y A\n  D A E I\n  L T A E\n  W E I E").stdout(">")

    '''

    @check("init3")
    def invalid_center(self):
        """3x3 board: move blank left (tile 1) then up (tile 4), then try to move tiles 1, 2, 6, 8"""
        child = self.spawn("./fifteen 3").stdin("1")                    \
                                         .stdout("Tile to move:")       \
                                         .stdin("4")                    \
                                         .stdout("8-7-6|5-0-3|2-4-1")   \
                                         .stdout("Tile to move:")

        for move in ["1", "2", "6"]:
            child.stdin(move).stdout("Illegal move.")
        child.stdin("8").stdout("8-7-6|5-0-3|2-4-1")

    @check("init3")
    def win_3x3(self):
        """3x3 board: make sure game is winnable"""
        moves = "34125876412587641241235476123748648578564567865478"
        child = self.spawn("./fifteen 3").stdout("Tile to move:")
        for move in moves[:-1]:
            child.stdin(move).stdout("Tile to move:")
        child.stdin(moves[-1]).stdout("1-2-3|4-5-6|7-8-0\n").exit(0)

    @check("compiles")
    def win_4x4(self):
        """4x4 board: make sure game is winnable"""
        moves = [
            "4", "5", "6", "1", "2", "4", "5", "6", "1", "2",
            "3", "7", "11", "10", "9", "1", "2", "3", "4", "5",
            "6", "8", "1", "2", "3", "4", "7", "11", "10", "9",
            "14", "13", "12", "1", "2", "3", "4", "14", "13",
            "12", "1", "2", "3", "4", "14", "13", "12", "1",
            "2", "3", "4", "12", "9", "15", "1", "2", "3", "4",
            "12", "9", "13", "14", "9", "13", "14", "7", "5", "9",
            "13", "14", "15", "10", "11", "5", "9", "13", "7", "11",
            "5", "9", "13", "7", "11", "15", "10", "5", "9", "13", "15",
            "11", "8", "6", "7", "8", "14", "12", "6", "7", "8", "14",
            "12", "6", "7", "8", "14", "15", "11", "10", "6", "7", "8",
            "12", "15", "11", "10", "15", "11", "14", "12", "11", "15",
            "10", "14", "15", "11", "12"
        ]

        child = self.spawn("./fifteen 4").stdout("15-14-13-12|11-10-9-8|7-6-5-4|3-2-1-0\n") \
                                         .stdout("Tile to move:")
        for move in moves[:-1]:
            child.stdin(move).stdout("Tile to move:")
        child.stdin(moves[-1]).stdout("1-2-3-4|5-6-7-8|9-10-11-12|13-14-15-0").exit(0)'''
