import check50

@check50.check()
def exists():
    """mario.py submitted"""
    check50.exists("mario.py")

@check50.check(exists)
def one_question():
    """prints one question mark when input is 1"""
    check50.run("python mario.py").stdin("1").stdout("^\?\n", "?\n")

@check50.check(exists)
def four_questions():
    """prints four question mark when input is 4"""
    check50.run("python mario.py").stdin("4").stdout("^\?\?\?\?\n", "????\n")

@check50.check(exists)
def eight_questions():
    """prints eight question mark when input is 8"""
    check50.run("python mario.py").stdin("8").stdout("^\?\?\?\?\?\?\?\?\n", "????????\n")
