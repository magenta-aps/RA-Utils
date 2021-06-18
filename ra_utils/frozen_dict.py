#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections.abc import Iterator
from collections.abc import Mapping
from functools import reduce
from operator import xor
from typing import Any
from typing import List
from typing import Optional
from typing import Union


def is_iterator(value: Any) -> bool:
    return isinstance(value, Iterator)


class FrozenDict(Mapping):
    """Hashable immutable dictionary."""

    def __init__(
        self,
        mapping_or_iterator: Optional[Union[Mapping, Iterator, List]] = None,
        **kwargs: Optional[Any]
    ) -> None:
        # Precondition check that only hashable types are passed in
        mapping_or_iterator = mapping_or_iterator or {}
        if isinstance(mapping_or_iterator, Mapping):
            for key, value in mapping_or_iterator.items():
                hash(key)
                hash(value)
        elif is_iterator(mapping_or_iterator):
            mapping_or_iterator = list(mapping_or_iterator)
            for item in mapping_or_iterator:
                hash(item)
        else:
            raise TypeError(str(type(mapping_or_iterator)) + " object is not iterable")

        for key, value in kwargs.items():
            hash(key)
            hash(value)

        self._raw_dict = dict(mapping_or_iterator, **kwargs)

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
        # Precondition ensure that all entries should already be hashable
        hashed_elements = map(hash, self.items())
        hashed_value = reduce(xor, hashed_elements, 0)
        return hashed_value


def frozendict(*args: Any, **kwargs: Optional[Any]) -> FrozenDict:
    return FrozenDict(*args, **kwargs)
