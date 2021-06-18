#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from collections import defaultdict
from inspect import signature
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from ra_utils.frozen_dict import frozendict

DictKeyType = TypeVar("DictKeyType")
DictValueType = TypeVar("DictValueType")

DictMapKeyReturnType = TypeVar("DictMapKeyReturnType")
DictMapValueReturnType = TypeVar("DictMapValueReturnType")


def dict_map(
    dicty: Dict[DictKeyType, DictValueType],
    key_func: Optional[
        Union[
            Callable[[DictKeyType], DictMapKeyReturnType],
            Callable[[DictKeyType, DictValueType], DictMapKeyReturnType],
        ]
    ] = None,
    value_func: Optional[
        Union[
            Callable[[DictValueType], DictMapValueReturnType],
            Callable[[DictValueType, DictKeyType], DictMapValueReturnType],
        ]
    ] = None,
) -> Dict[
    Union[DictKeyType, DictMapKeyReturnType],
    Union[DictValueType, DictMapValueReturnType],
]:
    """Map the dict values.

    Example:
        input_dict = {1: 1, 2: 2, 3: 3}
        output_dict = dict_map(input_dict, value_func=lambda value: value ** 2)
        self.assertEqual(output_dict, {1: 1, 2: 4, 3: 6})
        output_dict = dict_map(input_dict, key_func=lambda key: key ** 2)
        self.assertEqual(output_dict, {1: 1, 4: 2, 6: 3})

    Returns:
        dict: A dict where func has been applied to every value.
    """

    def identity(
        x: Union[DictKeyType, DictValueType]
    ) -> Union[DictKeyType, DictValueType]:
        return x

    def to_two_arg(
        func: Union[Callable[[Any], Any], Callable[[Any, Any], Any]]
    ) -> Callable[[Any, Any], Any]:
        sig = signature(func)
        params = sig.parameters
        if len(params) > 2:
            raise TypeError("Provided mapping function takes too many arguments")
        if len(params) < 1:
            raise TypeError("Provided mapping function takes too few arguments")
        if len(params) == 1:
            return lambda key, value: func(key)  # type: ignore
        return func  # type: ignore

    key_func = to_two_arg(key_func or identity)
    value_func = to_two_arg(value_func or identity)
    return dict(
        [(key_func(key, value), value_func(value, key)) for key, value in dicty.items()]
    )


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
