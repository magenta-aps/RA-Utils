#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections.abc import Hashable
from decimal import Decimal
from typing import Any

from ra_utils.dict_map import dict_map
from ra_utils.frozen_dict import frozendict


def is_hashable(value: Any) -> bool:
    """Check if input is hashable by attempting to hashing it."""
    try:
        hash(value)
    except TypeError:
        return False
    return True


def is_probably_hashable(value: Any) -> bool:
    """Check if input is probably hashable without hashing it."""
    return isinstance(value, Hashable)


def ensure_hashable(value: Any) -> Any:
    """Convert input into hashable equivalents if required."""
    if isinstance(value, dict):
        value = frozendict(
            dict_map(
                value,
                key_func=ensure_hashable,
                value_func=ensure_hashable,
            )
        )
    elif isinstance(value, set):
        value = frozenset(map(ensure_hashable, value))
    elif isinstance(value, list):
        value = tuple(map(ensure_hashable, value))
    elif isinstance(value, Decimal) and value.is_snan():
        return Decimal("nan")
    elif isinstance(value, slice):
        # Builtin and not an acceptable base type, so cannot be extended
        # I.e. it is impossible to make a 'frozenslice'.
        raise TypeError("slice cannot be made hashable")
    if not is_hashable(value):  # pragma: no cover
        raise TypeError(repr(value) + " is not hashable, please report this!")
    return value
