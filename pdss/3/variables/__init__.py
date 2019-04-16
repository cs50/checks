import check50

@check50.check()
def exists():
    """input.py submitted"""
    check50.exists("input.py")

@check50.check(exists)
def david():
    """responds to name David"""
    check50.run("python input.py").stdin("David").stdout("hello, David")

@check50.check(exists)
def maria():
    """responds to name Maria"""
    check50.run("python input.py").stdin("Maria").stdout("hello, Maria")
