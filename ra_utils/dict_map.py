#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import Callable
from typing import Dict
from typing import Optional

from more_itertools import unzip


def dict_map(
    dicty: Dict,
    key_func: Optional[Callable] = None,
    value_func: Optional[Callable] = None,
) -> Dict:
    """Map a dictionary's keys and values.

    Example:
        pow2 = lambda x: x**2
        input_dict = {1: 1, 2: 2, 3: 3}
        output_dict = dict_map(input_dict, value_func=pow2)
        self.assertEqual(output_dict, {1: 1, 2: 4, 3: 9})
        output_dict = dict_map(input_dict, key_func=pow2)
        self.assertEqual(output_dict, {1: 1, 4: 2, 9: 3})

    Note:
        Care must be taken for mapped keys to not destructively interfere with
        one another, i.e. the key_function should be a bijective function.

    Returns:
        dict: A dict where func has been applied to every value.
    """
    # Handle base-cases, i.e. empty dict and no transformation
    if not dicty:
        return dicty
    if key_func is None and value_func is None:
        return dicty

    keys, values = unzip(dicty.items())
    if key_func:
        keys = map(key_func, keys)
    if value_func:
        values = map(value_func, values)
    return dict(zip(keys, values))
