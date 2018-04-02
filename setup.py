import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

description="MS Bot Framework app takes user input and returned responses from Microsoft LUIS"
setup(
        name="echo-LUIS-bot",
        version="1.0",
        description=('A test of the integration between MS Bot Framework and Microsoft LUIS.'),
        long_description=read('README.md'),
        author="Dan Needles",
        author_email="dneedles@gmail.com",
        scripts=["echo-LUIS-bot"],
     )
