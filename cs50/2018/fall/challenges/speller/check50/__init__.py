import os
import re
import uuid

from check50 import *

class Challenge(Checks):

    @check()
    def exists(self):
        """dictionary.c and dictionary.h exist"""
        self.require("dictionary.c", "dictionary.h")
        self.add("speller.c", "dictionaries", "Makefile", "texts", "sols")

    @check("exists")
    def compiles(self):
        """speller compiles"""
        self.spawn("make").exit(0)

    @check("compiles")
    @valgrind
    def qualifies(self):
        """qualifies for Big Board"""
        try:

            # inject canary
            canary = str(uuid.uuid4())
            self.spawn("sed -i -e 's/CANARY/{}/' speller.c".format(canary)).exit(0)
            self.spawn("make -B").exit(0)

            # Run on aca.txt
            self.spawn("./speller dictionaries/large texts/aca.txt 0 > actual.out").exit(0, timeout=20)
            actual = open("actual.out").read().splitlines()
            expected = open("sols/aca.txt").read().splitlines()

            # check for canary
            if canary != actual[-1]:
                raise Error("Your Makefile doesn't seem to have compiled speller.c")
            del actual[-1]

            # Compare output line for line.
            if len(actual) != len(expected):
                raise Error("{} lines expected, not {}".format(len(expected), len(actual)))
            for actual_line, expected_line in zip(actual, expected):
                if actual_line != expected_line:
                    raise Error("expected {}, not {}".format(expected_line, actual_line))

        # Clear log to avoid clutter.
        except Error as e:
            self.log = []
            raise e
        self.log = []

    @check("qualifies")
    def benchmark(self):
        """passes benchmarking"""

        # Timing data.
        self.data["time"] = {
            "load": 0.0,
            "check": 0.0,
            "size": 0.0,
            "unload": 0.0
        }
        for text in os.listdir("texts"):
            out = self.spawn("./speller dictionaries/large texts/{} 1".format(text)).stdout(timeout=20)
            try:
                load, check, size, unload = map(float, out.split())
            except ValueError:
                self.log.append(out)
                e = Error("program has unexpected output or runtime error")
                e.helpers = "If your hash function is causing an integer overflow error, try removing -fsanitize=integer from CFLAGS in your Makefile!"
                raise e
            self.data["time"]["load"] += load
            self.data["time"]["check"] += check
            self.data["time"]["size"] += size
            self.data["time"]["unload"] += unload
        self.data["time"]["total"] = self.data["time"]["load"] + self.data["time"]["check"] + \
                                     self.data["time"]["size"] + self.data["time"]["unload"]


        # Memory data.
        self.spawn("valgrind --tool=massif --heap=yes --stacks=yes --massif-out-file=massif.out ./speller dictionaries/large texts/holmes.txt 1").stdout()
        f = open("massif.out")

        heap = 0
        stack = 0
        re_heap = re.compile("mem_heap_B=(\d+)")
        re_stack = re.compile("mem_stacks_B=(\d+)")
        for line in f:
            heap_match = re_heap.match(line)
            stack_match = re_stack.match(line)
            if heap_match:
                heap = max(heap, int(heap_match.groups()[0]))
            elif stack_match:
                stack = max(stack, int(stack_match.groups()[0]))

        self.data["memory"] = {
            "stack": stack,
            "heap": heap
        }
