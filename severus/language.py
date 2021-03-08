# -*- coding: utf-8 -*-
"""
    severus.language
    ----------------

    Provides language data wrapper.

    :copyright: 2020 Giovanni Barillari
    :license: BSD-3-Clause
"""

from __future__ import annotations

import json
import re

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from yaml import SafeLoader as ymlLoader, load as ymlload

from .datastructures import GroupData


class Language:
    __slots__ = ['_sources', '_strings', '_groups', '_encoding', 'get']
    _re_nkey = re.compile(r'n\d+')

    def __init__(
        self,
        data_path: Path,
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
        path: Path,
        filename_prefix: bool = True
    ):
        sources, filename_prefix_applicable = [], False
        if path.is_dir():
            filename_prefix_applicable = filename_prefix
            for file_path in path.iterdir():
                if file_path.suffix in [
                    '.json', '.yml', '.yaml'
                ]:
                    sources.append(file_path)
        elif path.is_file():
            sources.append(path)
        for source in sources:
            self._sources.append({
                'path': source,
                'mtime': source.stat().st_mtime,
                'prefix': filename_prefix_applicable
            })
            self._load_source(source, filename_prefix_applicable)

    def _load_source(
        self,
        path: Path,
        filename_prefix: bool = False
    ):
        ext = path.suffix
        if ext == '.json':
            with path.open("rt", encoding=self._encoding) as f:
                data = json.loads(f.read())
        elif ext in ['.yml', '.yaml']:
            with path.open("rt", encoding=self._encoding) as f:
                data = ymlload(f.read(), Loader=ymlLoader)
        else:
            raise RuntimeError(f'Invalid source format: {path}')
        prefix = filename_prefix and path.stem or None
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
            mtime = source['path'].stat().st_mtime
            if mtime != source['mtime']:
                source['mtime'] = mtime
                self._load_data(source['path'], source['prefix'])

    def _get_reload(self, text: str) -> Tuple[str, Dict[int, str]]:
        self._ensure_updated_sources()
        return self._strings.get(text, text), self._groups.get(text, {})

    def _get_static(self, text: str) -> Tuple[str, Dict[int, str]]:
        return self._strings.get(text, text), self._groups.get(text, {})
