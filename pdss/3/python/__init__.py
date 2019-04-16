import check50

@check50.check()
def exists():
    """hello.py submitted"""
    check50.exists("hello.py")

@check50.check(exists)
def hello():
    """says hello"""
    check50.run("python hello.py").stdout("hello, world")
