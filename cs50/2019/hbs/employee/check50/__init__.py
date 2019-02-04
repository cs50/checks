from check50 import *
import os


class Employee(Checks):

    @check()
    def exists(self):
        """employee.py submitted"""
        self.require("employee.py")
        self.add("1.csv", "2.csv", "3.csv")

    @check("exists")
    def consonants(self):
        """employee.py handles titles that begin with consonants"""
        os.rename("1.csv", "employee.csv")
        self.spawn("python employee.py").stdout("Andrew Adams is a General Manager\n")


    @check("exists")
    def vowels(self):
        """employee.py handles titles that begin with vowels"""
        os.rename("2.csv", "employee.csv")
        self.spawn("python employee.py").stdout("Laura Callahan is an IT Staff\n")

    @check("exists")
    def combination(self):
        """employee.py handles multiple titles"""
        os.rename("3.csv", "employee.csv")
        self.spawn("python employee.py").stdout("Andrew Adams is a General Manager\nLaura Callahan is an IT Staff\n")
