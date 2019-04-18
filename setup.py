#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="ccsdoc",
    version="0.0.1",
    description="Parser tools for generating CCS Java documentation",
    author="Alexandre Boucaud",
    author_email="aboucaud@apc.in2p3.fr",
    packages=find_packages(),
    license="BSD",
    python_requires='>=3.6',
    install_requires = [
        "click",
    ],
    entry_points = {
        "console_scripts": [
            "parse-commands = ccsdoc.scripts.cli:cli",
        ],
    },
    zip_safe=False,
)
