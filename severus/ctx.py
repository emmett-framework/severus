# -*- coding: utf-8 -*-
"""
    severus.ctx
    -----------

    Provides context facilities.

    :copyright: 2020 Giovanni Barillari
    :license: BSD-3-Clause
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Generic, Union

_ctx = ContextVar('ctx', default=None)
_lang = ContextVar('lang', default=None)


def set_context(translator: Generic) -> Token:
    return _ctx.set(translator)


def get_context() -> Union[Generic, None]:
    return _ctx.get()


def reset_context(token: Token):
    _ctx.reset(token)


@contextmanager
def context(translator: Generic):
    token = set_context(translator)
    yield
    reset_context(token)


def set_language(language: str) -> Token:
    return _lang.set(language)


def get_language() -> Union[str, None]:
    return _lang.get()


def reset_language(token: Token):
    _lang.reset(token)


@contextmanager
def language(language: str):
    token = set_language(language)
    yield
    reset_language(token)
