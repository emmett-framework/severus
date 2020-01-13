# -*- coding: utf-8 -*-
"""
    severus.translator
    ------------------

    Provides main translation interface.

    :copyright: 2020 Giovanni Barillari
    :license: BSD-3-Clause
"""

from __future__ import annotations

import os
import re

from typing import Dict, Optional

from .ctx import get_language
from .datastructures import Tstr
from .language import Language


class Translator:
    __slots__ = [
        '_langmap', '_languages',
        '_path', '_encoding', '_default_language',
        '_filename_prefix', '_changes_track', '_str_class'
    ]
    _re_langpath = re.compile(
        r'^[a-z]{2}([-_][a-zA-Z]{2})?(\.json|\.yml|\.yaml)?$'
    )

    def __init__(
        self,
        path: str,
        default_language: str = 'en',
        encoding: str = 'utf8',
        use_filename_as_prefix: bool = True,
        watch_changes: bool = False,
        str_class: Optional[Tstr] = Tstr
    ):
        self._langmap: Dict[str, str] = {}
        self._languages: Dict[str, Language] = {}
        self._path: str = path
        self._encoding: str = encoding
        self._default_language: str = default_language
        self._filename_prefix: bool = use_filename_as_prefix
        self._changes_track: bool = watch_changes
        if not issubclass(str_class, Tstr):
            raise RuntimeError(
                f'{str_class.__name__} should be a subclass of Tstr'
            )
        self._str_class: Tstr = str_class
        self._build_languages()

    def _build_languages(self):
        for path in os.listdir(self._path):
            lang_match = self._re_langpath.match(path)
            if not lang_match:
                continue
            lang_key = path[:2] + (lang_match.groups()[0] or '')
            self._langmap[lang_key] = lang_key
            self._languages[lang_key] = Language(
                os.path.join(self._path, path),
                self._encoding,
                self._filename_prefix,
                self._changes_track
            )
        self._langmap[self._default_language] = self._langmap.get(
            self._default_language
        ) or self._default_language
        self._languages[self._default_language] = self._languages.get(
            self._default_language
        ) or Language(
            os.path.join(self._path, self._default_language),
            self._encoding,
            self._filename_prefix,
            self._changes_track
        )

    def __call__(self, text: str, lang: Optional[str] = None) -> Tstr:
        return self._str_class(text, lang=lang)

    def _get_best_language(self, lang: Optional[str] = None) -> str:
        return self._langmap.get(
            lang or get_language(), self._default_language
        )

    def translate(
        self,
        text: str,
        lang: Optional[str] = None,
        *args,
        **kwargs
    ) -> str:
        lang = self._get_best_language(lang)
        text_match, dict_match = self._languages[lang].get(text)
        n = kwargs.get('n')
        if n and dict_match:
            text_match = dict_match.get(
                max(i for i in dict_match.nkeys if i <= n), text_match
            )
        elif dict_match:
            text_match = dict_match.get('_', text_match)
        return text_match.format(*args, **kwargs)
