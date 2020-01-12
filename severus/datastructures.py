# -*- coding: utf-8 -*-
"""
    severus.datastructures
    ----------------------

    Provides datastructures for translator.

    :copyright: 2020 Giovanni Barillari
    :license: BSD-3-Clause
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

from .ctx import get_context


class Tstr:
    __slots__ = ['text', 'lang', 'args', 'kwargs']

    def __init__(self, text: str, lang: Optional[str] = None, *args, **kwargs):
        self.text = text
        self.lang = lang
        self.args = args
        self.kwargs = kwargs

    def format(self, *args, **kwargs) -> Tstr:
        data = dict(self.kwargs)
        data.update(kwargs)
        return self.__class__(self.text, self.lang, *args, **data)

    def __mod__(self, symbols: Union[Dict, Tuple]) -> Tstr:
        if isinstance(symbols, tuple):
            return self.format(*symbols)
        elif isinstance(symbols, dict):
            return self.format(**symbols)
        else:
            return self.format(*[symbols])

    def __getitem__(self, val: int) -> str:
        return str(self)[val]

    def __len__(self) -> int:
        return len(self.text)

    def __bool__(self) -> bool:
        return bool(self.text)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        return str(self) == other

    def __ne__(self, other: Any) -> bool:
        return str(self) != other

    def __add__(self, other: Any) -> str:
        return str(self) + str(other)

    def __radd__(self, other: Any) -> str:
        return str(other) + str(self)

    def __mul__(self, val) -> str:
        return str(self) * val

    def __str__(self) -> str:
        return get_context().translate(
            self.text, self.lang, *self.args, **self.kwargs
        )

    def __repr__(self):
        return repr(str(self))

    def encode(self, *args, **kwargs) -> bytes:
        return str(self).encode(*args, **kwargs)


class GroupData(dict):
    __slots__ = ['nkeys']

    def __init__(self, data: Dict[str, str]):
        kset = set(data.keys()) - {'_'}
        inner = {int(key[1:]): data[key] for key in kset}
        if '_' in data:
            inner['_'] = data['_']
        super().__init__(inner)
        self.nkeys = sorted([int(key[1:]) for key in kset])
