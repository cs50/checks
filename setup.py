from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    name="check50-checks",
    include_package_data=True,
    package_data = { '': ['*'] },
)

