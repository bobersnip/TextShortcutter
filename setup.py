#!/usr/bin/env python3
"""
Setup script for TextShortcutter
"""

import sys
import os
from pathlib import Path
from setuptools import setup, find_packages

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements_file = this_directory / "requirements.txt"
install_requires = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        install_requires = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="TextShortcutter",
    version="1.0.0",
    author="Convenience Culture LLC",
    author_email="convenienceculturellc@gmail.com",
    description="A secure text expander application with configurable trigger keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobersnip/TextShortcutter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'textshortcutter=main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
