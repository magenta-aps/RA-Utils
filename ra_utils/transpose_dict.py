#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import Any
from typing import Dict
from typing import Tuple
from typing import TypeVar

from ra_utils.dict_map import dict_map
from ra_utils.frozen_dict import frozendict


DictKeyType = TypeVar("DictKeyType")
DictValueType = TypeVar("DictValueType")


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
    hash(value)
    return value


def transpose_dict(
    mydict: Dict[DictKeyType, DictValueType]
) -> Dict[DictValueType, Tuple[DictKeyType, ...]]:
    """Transpose a dictionary, such that keys become values and values become keys.

    **XXX: Currently broken, awaiting fix:
        <a href="https://git.magenta.dk/rammearkitektur/ra-utils/-/merge_requests/8">
            MR
        </a>
    **

    *Note: Keys actually become a list of values, rather than plain values, as value
           uniqueness is not guaranteed, and thus multiple keys may have the same
           value.*

    Example:
        ```Python
        test_dict = {'test_key1': 'test_value1'}
        tdict = transpose_dict(test_dict)
        assert tdict == {"test_value1": ["test_key1"]}
        ```

    Example:
        ```Python
        test_dict = {
            "test_key1": "test_value1",
            "test_key2": "test_value2",
            "test_key3": "test_value1",
        }
        tdict = transpose_dict(test_dict)
        assert tdict == {
            "test_value1": ["test_key1", "test_key3"],
            "test_value2": ["test_key2"]
        }
        ```

    Args:
        mydict: Dictionary to be transposed.

    Returns:
        Tranposed dictionary.
    """

    # Ensure all values are hashable
    hashdict = dict_map(mydict, value_func=ensure_hashable)
    # Reverse the dict
    reversed_dict: Dict[DictValueType, Tuple[DictKeyType, ...]] = dict()
    for key, value in hashdict.items():
        reversed_dict[value] = reversed_dict.get(value, ()) + (key,)
    return reversed_dict
