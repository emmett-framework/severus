# -*- coding: utf-8 -*-
"""
severus.apis
------------

Provides APIs for main usage.

:copyright: 2020 Giovanni Barillari
:license: BSD-3-Clause
"""

from __future__ import annotations

import os
from typing import Optional

from .ctx import set_context, set_language
from .translator import Translator


class Severus(Translator):
    def __init__(
        self,
        path: Optional[str] = None,
        default_language: str = "en",
        encoding: str = "utf8",
        use_filename_as_prefix: bool = True,
        watch_changes: bool = False,
    ):
        super().__init__(path or os.getcwd(), default_language, encoding, use_filename_as_prefix, watch_changes)
        set_context(self)
        set_language(self._default_language)
