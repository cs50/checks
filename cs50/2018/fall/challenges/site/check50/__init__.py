from check50 import *


class Site(Checks):

    @check()
    def submitted(self):
        """site deployed to https://USERNAME.cs50.site"""
