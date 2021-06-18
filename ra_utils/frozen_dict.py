#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections.abc import Mapping
from functools import reduce
from operator import xor
from typing import Any
from typing import Iterator
from typing import Optional

import ra_utils.ensure_hashable
from ra_utils.dict_map import dict_map


class FrozenDict(Mapping):
    """Hashable immutable dictionary."""

    def __init__(self, *args: Any, **kwargs: Optional[Any]) -> None:
        ensure_hashable = ra_utils.ensure_hashable.ensure_hashable
        self._raw_dict = dict_map(
            dict(*args, **kwargs),
            key_func=ensure_hashable,
            value_func=ensure_hashable,
        )

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
        # The order of the elements does not matter, since we are using xor to reduce
        hashed_elements = map(hash, self.items())
        hashed_value = reduce(xor, hashed_elements, 0)
        return hashed_value


def frozendict(*args: Any, **kwargs: Optional[Any]) -> FrozenDict:
    return FrozenDict(*args, **kwargs)
