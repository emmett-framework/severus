# -*- coding: utf-8 -*-
"""
    severus.language
    ----------------

    Provides language data wrapper.

    :copyright: 2020 Giovanni Barillari
    :license: BSD-3-Clause
"""

from __future__ import annotations

import io
import json
import os
import re

from typing import Any, Dict, List, Optional, Tuple, Union
from yaml import SafeLoader as ymlLoader, load as ymlload

from .datastructures import GroupData


class Language:
    __slots__ = ['_sources', '_strings', '_groups', '_encoding', 'get']
    _re_nkey = re.compile(r'n\d+')

    def __init__(
        self,
        data_path: str,
        encoding: str = 'utf8',
        filename_prefix: bool = True,
        watch_changes: bool = False
    ):
        self._sources: List[Dict[str, Any]] = []
        self._strings: Dict[str, str] = {}
        self._groups: Dict[Union[int, str], str] = {}
        self._encoding: str = encoding
        self.get = self._get_reload if watch_changes else self._get_static
        self._load_sources(data_path, filename_prefix)

    def _build_key(self, key: str, prefix: Optional[str] = None):
        return f'{prefix}.{key}' if prefix else key

    def _load_sources(
        self,
        path: str,
        filename_prefix: bool = True
    ):
        sources, filename_prefix_applicable = [], False
        if os.path.isdir(path):
            filename_prefix_applicable = filename_prefix
            for file_name in os.listdir(path):
                if os.path.splitext(file_name)[1] in [
                    '.json', '.yml', '.yaml'
                ]:
                    sources.append(os.path.join(path, file_name))
        elif os.path.isfile(path):
            sources.append(path)
        for source in sources:
            self._sources.append({
                'path': source,
                'mtime': os.stat(source).st_mtime,
                'prefix': filename_prefix_applicable
            })
            self._load_source(source, filename_prefix_applicable)

    def _load_source(
        self,
        path: str,
        filename_prefix: bool = False
    ):
        file_name, ext = os.path.splitext(path)
        if ext == '.json':
            with io.open(path, 'rt', encoding=self._encoding) as f:
                data = json.loads(f.read())
        elif ext in ['.yml', '.yaml']:
            with io.open(path, 'rt', encoding=self._encoding) as f:
                data = ymlload(f.read(), Loader=ymlLoader)
        else:
            raise RuntimeError(f'Invalid source format: {path}')
        prefix = filename_prefix and file_name.rsplit('/', 1)[-1] or None
        self._load_data(data, prefix)

    def _load_data(
        self,
        data: Dict[str, Union[Dict, str]],
        prefix: Optional[str] = None
    ):
        for key, val in data.items():
            if isinstance(val, str):
                self._strings[self._build_key(key, prefix)] = val
                continue
            keyset = set(val.keys()) - {'_'}
            if len(self._re_nkey.findall(','.join(keyset))) == len(keyset):
                self._groups[self._build_key(key, prefix)] = GroupData(val)
            else:
                self._load_data(val, self._build_key(key, prefix))

    def _ensure_updated_sources(self):
        for source in self._sources:
            mtime = os.stat(source['path']).st_mtime
            if mtime != source['mtime']:
                source['mtime'] = mtime
                self._load_data(source['path'], source['prefix'])

    def _get_reload(self, text: str) -> Tuple[str, Dict[int, str]]:
        self._ensure_updated_sources()
        return self._strings.get(text, text), self._groups.get(text, {})

    def _get_static(self, text: str) -> Tuple[str, Dict[int, str]]:
        return self._strings.get(text, text), self._groups.get(text, {})
