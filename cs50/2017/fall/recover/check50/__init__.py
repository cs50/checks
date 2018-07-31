from check50 import *
import os
import re

class Recover(Checks):


    def initialize_data(self):
        """reads hashes and sizes of jpegs from files into dicts"""
        self.add("hashes.txt")
        self.add("sizes.txt")

        # a regular expression to capture data and filename surrounded by whitespace
        parser = re.compile("^\s*(\S*)\s*(\S*.jpg)\s*$")

        # parse jpg hashes from file
        self.hashes = dict()
        with open("hashes.txt", "r") as hash_file:
            for line in hash_file.read().split("\n"):
                match = parser.match(line)
                if match:
                    # add dict entry with filename as key and hash as value
                    self.hashes[match.group(2)] = match.group(1)

        # parse jpg sizes from file
        self.sizes = dict()
        with open("sizes.txt", "r") as size_file:
            for line in size_file.read().split("\n"):
                match = parser.match(line)
                if match:
                    # add dict entry with filename as key and size in bytes as value
                    self.sizes[match.group(2)] = int(match.group(1))

    @check()
    def exists(self):
        """recover.c exists."""
        self.require("recover.c")

    @check("exists")
    def compiles(self):
        """recover.c compiles."""
        self.spawn("clang -std=c11 -o recover recover.c -lcs50 -lm").exit(0)

    @check("compiles")
    def test_noimage(self):
        """handles lack of forensic image"""
        self.spawn("./recover").exit(1)

    @check("compiles")
    def first_image(self):
        """recovers 000.jpg correctly"""
        self.initialize_data()
        self.add("card.raw")
        self.spawn("./recover card.raw").exit(0, timeout=10)
        self.check_jpg("000.jpg")

    @check("compiles")
    def middle_images(self):
        """recovers middle images correctly"""
        self.initialize_data()
        self.add("card.raw")
        self.spawn("./recover card.raw").exit(0, timeout=10)
        for i in range(1, 49):
            self.check_jpg("{:03d}.jpg".format(i))

    @check("compiles")
    def last_image(self):
        """recovers 049.jpg correctly"""
        self.initialize_data()
        self.add("card.raw")
        self.spawn("./recover card.raw").exit(0, timeout=10)
        self.check_jpg("049.jpg")

    def check_jpg(self, jpg):
        """Checks for a jpeg to have the correct hash, and if it does not,
        raises and error with a helpful hint"""
        self.require(jpg)

        # pass test if jpeg is correct
        if self.hash(jpg) == self.hashes[jpg]:
            return

        err = Error("recovered image does not match")

        # read jpeg header as a byte array and throw out extra bits
        with open(jpg, "rb") as f:
            header = bytearray(f.read(4))
        if len(header) >= 4:
            header[3] = header[3] & 0xf0

        # test that the jpeg header is correct
        correct = b'\xff\xd8\xff\xe0'
        if header != correct:
            header_str = " ".join(["0x{:02x}".format(b) for b in header])
            correct_str =  " ".join(["0x{:02x}".format(b) for b in correct])
            helper = "It looks like {} starts with {} instead of {}."
            err.helpers = helper.format(jpg, header_str, correct_str)
            raise err

        # test that jpeg length is correct
        jpg_size = os.path.getsize(jpg)
        if jpg_size != self.sizes[jpg]:
            helper = "Expected {} to be {} bytes, but it's instead {} bytes."
            err.helpers = helper.format(jpg, jpg_size, self.sizes[jpg])
            raise err
