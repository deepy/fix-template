#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fix_template",
    version="0.0.1",
    author="Alex Nordlund",
    author_email="deep.alexander@gmail.com",
    description="FIX repository tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepy/fix-template",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
)