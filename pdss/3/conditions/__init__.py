import check50

@check50.check()
def exists():
    """mario.py exists."""
    check50.exists("mario.py")

@check50.check(exists)
def test_reject_negative():
    """rejects a height of -1"""
    check50.run("python mario.py").stdin("-1").reject()

@check50.check(exists)
def test_reject_zero():
    """rejects a height of 0"""
    check50.run("python mario.py").stdin("0").reject()

@check50.check(exists)
def test_reject_5():
    """rejects a height of 5"""
    check50.run("python mario.py").stdin("5").reject()

@check50.check(exists)
def test_reject_large():
    """rejects a height of 28"""
    check50.run("python mario.py").stdin("28").reject()

@check50.check(exists)
def test1():
    """handles a height of 1 correctly"""
    check50.run("python mario.py").stdin("1").stdout("^#\n$", "#\n")

@check50.check(exists)
def test2():
    """handles a height of 2 correctly"""
    check50.run("python mario.py").stdin("2").stdout("^#\n#\n$", "#\n#\n")

@check50.check(exists)
def test4():
    """handles a height of 4 correctly"""
    check50.run("python mario.py").stdin("4").stdout("^#\n#\n#\n#\n$", "#\n#\n#\n#\n")
