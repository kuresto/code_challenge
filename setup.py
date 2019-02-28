# coding: utf-8
import os
from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

setup_requires = parse_requirements(
    os.path.join(ROOT, "requirements", "base.txt"), session="hack"
)
setup_requires = [str(ir.req) for ir in setup_requires]

setup(
    name="Bluestorm API",
    version="0.0.1",
    author="Nilton Teixeira",
    author_email="niltonfrederico@gmail.com",
    url="",
    description="",
    long_description=open(os.path.join(ROOT, "README.md"), "r", encoding="utf8").read(),
    setup_requires=setup_requires,  # required packages (this only download required packages)
    install_requires=setup_requires,  # install required packages
    zip_safe=True,
    include_package_data=True,
)
