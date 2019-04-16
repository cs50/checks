import check50

@check50.check()
def exists():
    """print.py submitted"""
    check50.exists("print.py")

@check50.check(exists)
def prints_something():
    """prints output"""
    result = check50.run("python print.py").stdout()
    if result.strip() == "":
        raise check50.Failure("no output found")

@check50.check(prints_something)
def doesnt_print_hello():
    """prints something other than hello, world"""
    result = check50.run("python print.py").stdout()
    if result.strip() == "hello, world":
        raise check50.Failure("printed hello world")
