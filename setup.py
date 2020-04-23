import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="fnbr-api",
    version="1.1.4",
    author="Douile",
    description="Python wrapper of the fnbr.co fortnite shop API for ease of use in a python enviroment.",
    long_description=read("README.rst"),
    long_description_content_type='text/x-rst',
    license="MIT",
    keywords="API fortnite fnbr",
    packages=["fnbr","aiofnbr"],
    install_requires=["requests","aiohttp"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    url="https://github.com/Douile/fnbr-api",
    project_urls={
        'Documentation': 'https://github.com/Douile/fnbr-api/wiki',
        'Source': 'https://github.com/Douile/fnbr-api/'
    },
)
