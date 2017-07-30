import os
from setuptools import setup, find_packages
import sys

def main():
    setup(
        name="check50-checks",
        include_package_data=True,
        **setup50()
    )


def setup50():
    if sys.version_info >= (3, 3):
        with open("MANIFEST.in", "w") as f:
            f.write("graft checks\n")
        return {"packages": ["checks"]}

    with open("checks/__init__.py", "w") as f:
        f.write("__path__ = __import__(\"pkgutil\").extend_path(__path__, __name__)\n")

    for root, dirs, files in os.walk("checks"):
        if not "__init__.py" in files:
            print(os.path.join(root, "__init__.py"))
    return {"packages": find_packages(), "package_data": { "": "*" }}


if __name__ == "__main__":
    main()
