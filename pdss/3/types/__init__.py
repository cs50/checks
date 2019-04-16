import check50

@check50.check()
def exists():
    """types.py submitted"""
    check50.exists("types.py")

@check50.check(exists)
def positives():
    """computes 1 + 1 as 2"""
    check50.run("python types.py").stdin("1").stdin("1").stdout("2")

@check50.check(exists)
def zero():
    """computes 5 + 0 as 5"""
    check50.run("python types.py").stdin("5").stdin("0").stdout("5")

@check50.check(exists)
def negative():
    """computes -10 + 38 as 28"""
    check50.run("python types.py").stdin("-10").stdin("38").stdout("28")
