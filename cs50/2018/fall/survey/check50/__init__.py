from check50 import *
from functools import wraps


def helper(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, "app"):
            self.app = self.flask(Survey.APP)
        return f(self, *args, **kwargs)
    return wrapper


class Survey(Checks):

    APP = "application.py"


    @helper
    def get_content(self, route, tag="input"):
        content = self.app.get(route).content()
        return content.find_all(tag)


    @check()
    def exists(self):
        """application.py exists"""
        self.require("application.py")


    @check("exists")
    def startup(self):
        """application starts up"""
        self.flask(Survey.APP).get("/").status(200)


    @check("startup")
    def has_form(self):
        """has form"""

        if len(self.get_content("/", "form")) < 1:
            raise Error("expected form element")


    @check("has_form")
    def has_text_fields(self):
        """has one or more text fields"""

        inputs = self.get_content("/", "form")[0].find_all("input")
        if len(tuple(filter(lambda e: e.attrs["type"] == "text", inputs))) < 1:
            raise Error("expected at least one text input")


    @check("has_form")
    def has_checkbox_or_radio_buttons(self):
        """has one or more checkboxes or two or more radio buttons"""

        inputs = self.get_content("/", "form")[0].find_all("input")
        if len(tuple(filter(lambda e: e.attrs["type"] == "checkbox", inputs))) < 1 and \
            len(tuple(filter(lambda e: e.attrs["type"] == "radio", inputs))) < 2:
            raise Error("expected at least one checkbox or two radio buttons")


    @check("has_form")
    def has_select_and_options(self):
        """has one or more select menus, each with two or more options"""

        selects = self.get_content("/", "form")[0].find_all("select")
        if len(selects) < 1 or \
            any((len(select.find_all("option")) < 2 for select in selects)):
            raise Error("expected one or more select menus, each with two or more options")
