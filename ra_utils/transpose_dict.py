#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections import defaultdict
from typing import Any
from typing import Dict
from typing import List
from typing import TypeVar

from ra_utils.frozen_dict import frozendict

DictKeyType = TypeVar("DictKeyType")
DictValueType = TypeVar("DictValueType")


def ensure_hashable(value: Any) -> Any:
    """Convert input into hashable equivalents if required."""
    if isinstance(value, dict):
        value = frozendict(**value)
    elif isinstance(value, set):
        value = frozenset(value)
    elif isinstance(value, list):
        value = tuple(value)
    hash(value)
    return value


def transpose_dict(
    mydict: Dict[DictKeyType, DictValueType]
) -> Dict[DictValueType, List[DictKeyType]]:
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
    reversed_dict = defaultdict(list)
    for key, value in mydict.items():
        reversed_dict[ensure_hashable(value)].append(key)
    return dict(reversed_dict)
