import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
setup (
    name = "filebase-qt4",
    version = "0.0.0.dev1",
    
    description = ("A program that can parse and query files in FileBase."),
    long_description = read("README.md"),
    
    url = "https://github.com/filebase/filebase-qt4",
    
    author = "Bora Mert Alper",
    author_email = "boramalper@gmail.com",
    
    packages = ["filebase", "filebase_qt4"],

    scripts=["bin/filebase-qt4"],
   
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
    ],
)
