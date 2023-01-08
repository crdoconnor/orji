# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
from sys import version_info, stderr, exit
import codecs
import sys
import os


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    ) as f:
        return f.read()


setup(
    name="orji",
    version=read("VERSION").replace("\n", ""),
    description="Org mode to jinja2 templating",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing :: Markup",
        "Topic :: Software Development :: Libraries",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
    ],
    keywords="orgmode markdown latex jinja2",
    author="Colm O'Connor",
    author_email="colm.oconnor.github@gmail.com",
    url="http://hitchdev.com/orji/",
    license="MIT",
    install_requires=[
        "orgparse>=0.3.1",
        "jinja2>=3.1.2",
        "click>=8.1.3",
        "python-slugify>=7.0.0",
    ],
    packages=find_packages(
        exclude=[
            "tests",
            "docs",
            "hitch",
        ]
    ),
    package_data={},
    zip_safe=False,
    include_package_data=True,
    entry_points={"console_scripts": ["orji = orji:main"]},
)
