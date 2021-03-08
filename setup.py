import io
import re

from setuptools import setup


with io.open("severus/__version__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="Severus",
    version=version
)
