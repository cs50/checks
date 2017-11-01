from check50 import *
from functools import wraps


def helper(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "app"):
            self.app = self.flask(Finance.APP)
        return f(self, *args, **kwargs)
    return wrapper


class Finance(Checks):

    APP = "application.py"

    @helper
    def register(self, username, password, confirmation):
        """Helper functoin for registering user"""
        form = {"username": username, "password": password, "confirmation": confirmation}
        return self.app.post("/register", data=form)

    @helper
    def login(self, username, password):
        """Helper function for logging in"""
        return self.app.post("/login", data={"username": username, "password": password})

    @helper
    def validate_form(self, route, fields, field_tag="input"):
        """Make sure HTML form at `route` has input fields given by `fields`"""
        if not isinstance(fields, list):
            fields = [fields]

        content = self.app.get(route).content()
        required = {field: False for field in fields}
        for tag in content.find_all(field_tag):
            try:
                name = tag.attrs["name"]
                if required[name]:
                    raise Error("found more than one field called \"{}\"".format(name))
            except KeyError:
                pass
            else:
                self.log.append("found required \"{}\" field".format(name))
                required[name] = True

        try:
            missing = next(name for name, found in required.items() if not found)
        except StopIteration:
            pass
        else:
            raise Error("expected to find {} field with name \"{}\", but none found".format(field_tag, missing))

        if content.find("button", type="submit") is None:
            raise Error("expected button to submit form, but none was found")

    @helper
    def login(self, username, password):
        """Checks that user can log in"""
        return self.app.post("/login", data={"username": username, "password": password})

    @helper
    def quote(self, ticker):
        """Checks that getting a quote results in desired outcome"""
        return self.app.post("/quote", data={"symbol": ticker})

    @helper
    def transaction(self, route, symbol, shares):
        return self.app.post("{}".format(route), data={"symbol": symbol, "shares": shares})

    @check()
    def exists(self):
        """application.py exists"""
        self.require("application.py")
        self.add("lookup.py")
        self.append_code("helpers.py", "lookup.py")

    @check("exists")
    def startup(self):
        """application starts up"""
        self.flask(Finance.APP).get("/").status(200)

    @check("startup")
    def register_page(self):
        """register page has all required elements"""
        self.validate_form("/register", ["username", "password", "confirmation"])

    @check("register_page")
    def simple_register(self):
        """registering user succeeds"""
        self.register("cs50", "ohHai28!", "ohHai28!").status(200)

    @check("register_page")
    def register_empty_field_fails(self):
        """registration with an empty field fails"""
        for user in [("", "crimson", "crimson"), ("jharvard", "crimson", ""), ("jharvard", "", "")]:
            self.register(*user).status(400)

    @check("register_page")
    def register_password_mismatch_fails(self):
        """registration with password mismatch fails"""
        self.register("check50user1", "thisiscs50", "crimson").status(400)

    @check("register_page")
    def register_reject_duplicate_username(self):
        """registration rejects duplicate username"""
        user = ["elfie", "Doggo28!", "Doggo28!"]
        self.register(*user).status(200)
        self.register(*user).status(400)

    @check("startup")
    def login_page(self):
        """login page has all required elements"""
        self.validate_form("/login", ["username", "password"])

    @check("simple_register")
    def can_login(self):
        """logging in as registered user succceeds"""
        self.login("cs50", "ohHai28!").status(200).get("/", follow_redirects=False).status(200)

    @check("can_login")
    def quote_page(self):
        """quote page has all required elements"""
        self.login("cs50", "ohHai28!")
        self.validate_form("/quote", "symbol")

    @check("quote_page")
    def quote_handles_invalid(self):
        """quote handles invalid ticker symbol"""
        self.login("cs50", "ohHai28!")
        self.quote("ZZZ").status(400)

    @check("quote_page")
    def quote_handles_blank(self):
        """quote handles blank ticker symbol"""
        self.login("cs50", "ohHai28!")
        self.quote("").status(400)

    @check("quote_page")
    def quote_handles_valid(self):
        """quote handles valid ticker symbol"""
        self.login("cs50", "ohHai28!")
        self.quote("AAAA").status(200).content(r"28\.00", "28.00", name="body")

    @check("can_login")
    def buy_page(self):
        """buy page has all required elements"""
        self.login("cs50", "ohHai28!")
        self.validate_form("/buy", ["shares", "symbol"])

    @check("buy_page")
    def buy_handles_invalid(self):
        """buy handles invalid ticker symbol"""
        self.login("cs50", "ohHai28!")
        self.transaction("/buy", "ZZZZ", "2").status(400)

    @check("buy_page")
    def buy_handles_incorrect_shares(self):
        """buy handles fractional, negative, and non-numeric shares"""
        self.login("cs50", "ohHai28!")
        self.transaction("/buy", "AAAA", "-1").status(400)
        self.transaction("/buy", "AAAA", "1.5").status(400)
        self.transaction("/buy", "AAAA", "foo").status(400)

    @check("buy_page")
    def buy_handles_valid(self):
        """buy handles valid purchase"""
        self.login("cs50", "ohHai28!")
        self.transaction("/buy", "AAAA", "4").content(r"112\.00", "112.00").content(r"9,?888\.00", "9,888.00")

    @check("buy_handles_valid")
    def sell_page(self):
        """sell page has all required elements"""
        self.login("cs50", "ohHai28!")
        self.validate_form("/sell", ["shares"])
        self.validate_form("/sell", ["symbol"], field_tag="select")

    @check("buy_handles_valid")
    def sell_handles_invalid(self):
        """sell handles invalid number of shares"""
        self.login("cs50", "ohHai28!")
        self.transaction("/sell", "AAAA", "8").status(400)

    @check("buy_handles_valid")
    def sell_handles_valid(self):
        """sell handles valid sale"""
        self.login("cs50", "ohHai28!")
        self.transaction("/sell", "AAAA", "2").content("56\.00", "56.00").content(r"9,?944\.00", "9,944.00")
