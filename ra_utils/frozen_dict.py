#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections.abc import Mapping
from typing import Any
from typing import Iterator
from typing import Optional


class FrozenDict(Mapping):
    """Hashable immutable dictionary."""

    def __init__(self, *args: Any, **kwargs: Optional[Any]) -> None:
        self._raw_dict = dict(*args, **kwargs)
        self._hash = None

    def __getitem__(self, key: Any) -> Any:
        value = self._raw_dict.__getitem__(key)
        return value

    def __str__(self) -> str:
        return str(self._raw_dict)

    def __repr__(self) -> str:
        return repr(self._raw_dict)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._raw_dict)

    def __len__(self) -> int:
        return len(self._raw_dict)

    def __hash__(self) -> int:
        return hash(tuple(sorted(self._raw_dict.items())))
