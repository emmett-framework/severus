# -*- coding: utf-8 -*-

import io
import re

from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("severus/__version__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

with io.open("requirements.txt", "rt", encoding="utf8") as f:
    requirements = f.readlines()


setup(
    name="Severus",
    version=version,
    url="https://github.com/emmett-framework/severus",
    project_urls={
        "Code": "https://github.com/emmett-framework/severus",
        "Issue tracker": "https://github.com/emmett-framework/severus/issues",
    },
    license="BSD-3-Clause",
    author="Giovanni Barillari",
    author_email="gi0baro@d4net.org",
    description="An internationalization engine designed with simplicity in mind",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
