from check50 import *

class Music(Checks):

    @check()
    def exists(self):
        """bday.txt and helpers.c exist"""

        # Ensure student files exist
        self.require("bday.txt")
        self.require("helpers.c")

        # Include distribution code
        self.add("helpers.h")
        self.add("wav.h")
        self.add("wav.c")

        # Include testing code
        self.add("is_rest.c")
        self.add("duration.c")
        self.add("frequency.c")

    @check("exists")
    def compiles(self):
        """helpers.c compiles"""
        self.spawn("clang -std=c11 -o is_rest is_rest.c wav.c helpers.c -lcs50 -lm").exit(0)
        self.spawn("clang -std=c11 -o duration duration.c wav.c helpers.c -lcs50 -lm").exit(0)
        self.spawn("clang -std=c11 -o frequency frequency.c wav.c helpers.c -lcs50 -lm").exit(0)

    @check("exists")
    def bday(self):
        """bday.txt is correct"""
        solution = ["D4@1/8", "D4@1/8", "E4@1/4", "D4@1/4", "G4@1/4", "F#4@1/2",
                    "D4@1/8", "D4@1/8", "E4@1/4", "D4@1/4", "A4@1/4", "G4@1/2",
                    "D4@1/8", "D4@1/8", "D5@1/4", "B4@1/4", "G4@1/4", "F#4@1/4",
                    "E4@1/4", "C5@1/8", "C5@1/8", "B4@1/4", "G4@1/4", "A4@1/4",
                    "G4@1/2"]
        try:
            bday = open("bday.txt").read().splitlines()
        except Exception:
            raise Error("bday.txt is not valid text file")

        # Check length of song
        if len(solution) != len(bday):
            raise Error("Expected {} lines in bday.txt, but yours has {}".format(len(solution), len(bday)))

        # Make sure each note matches
        note = 1
        for expected, actual in zip(solution, bday):
            if expected != actual:
                raise Error("Incorrect note on line {}".format(note))
            note += 1

    @check("compiles")
    def is_rest_true(self):
        """is_rest identifies "" as a rest"""
        exit = self.spawn("./is_rest ''").exit()
        if exit != 0:
            raise Error("Incorrectly identifies \"\" as a note")

    @check("compiles")
    def is_rest_false(self):
        """is_rest identifies "A4" as not a rest"""
        exit = self.spawn("./is_rest A4").exit()
        if exit != 1:
            raise Error("Incorrectly identifies \"A4\" as a rest")

    @check("compiles")
    def duration_eighth(self):
        """fraction of "1/8" returns duration 1"""
        actual = self.spawn("./duration 1/8").stdout().strip()
        expected = "1"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def duration_quarter(self):
        """fraction of "1/4" returns duration 2"""
        actual = self.spawn("./duration 1/4").stdout().strip()
        expected = "2"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def duration_dotted_quarter(self):
        """fraction of "3/8" returns duration 3"""
        actual = self.spawn("./duration 3/8").stdout().strip()
        expected = "3"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def duration_half(self):
        """fraction of "1/2" returns duration 4"""
        actual = self.spawn("./duration 1/2").stdout().strip()
        expected =  "4"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_A4(self):
        """note A4 has frequency 440"""
        actual = self.spawn("./frequency A4").stdout().strip()
        expected = "440"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_A6(self):
        """note A6 has frequency 1760"""
        actual = self.spawn("./frequency A6").stdout().strip()
        expected = "1760"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_ASharp5(self):
        """note A#5 has frequency 932"""
        actual = self.spawn("./frequency A#5").stdout().strip()
        expected = "932"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_AFlat3(self):
        """note Ab3 has frequency 208"""
        actual = self.spawn("./frequency Ab3").stdout().strip()
        expected = "208"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_C3(self):
        """note C3 has frequency 131"""
        actual = self.spawn("./frequency C3").stdout().strip()
        expected = "131"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequency_Bb5(self):
        """note Bb5 has frequency 932"""
        actual = self.spawn("./frequency Bb5").stdout().strip()
        expected = "932"
        if expected != actual:
            raise Error(Mismatch(expected, actual))

    @check("compiles")
    def frequencies(self):
        """produces all correct notes for octaves 3-5"""
        self.add("frequencies.txt")
        actual = open("frequencies.txt").read().splitlines()
        for line in actual:
            note, frequency = line.strip().split(": ")
            output = self.spawn("./frequency {}".format(note)).stdout().strip()
            expected = str(frequency)
            if output != expected:
                raise Error("Incorrect frequency for {}, should be {}, not {}".format(
                    note, expected, output))
