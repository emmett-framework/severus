# -*- coding: utf-8 -*-

import os

import pytest

from severus.translator import Translator


@pytest.fixture(scope="session")
def T():
    return Translator(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang1"))


@pytest.fixture(scope="session")
def Tpre():
    return Translator(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang2"))
