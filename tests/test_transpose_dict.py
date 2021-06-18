#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import pytest

from ra_utils.frozen_dict import frozendict
from ra_utils.transpose_dict import dict_map
from ra_utils.transpose_dict import transpose_dict


def test_dict_map():
    assert dict_map({}) == {}
    assert dict_map({"a": "b"}) == {"a": "b"}

    input_dict = {1: 1, 2: 2, 3: 3}
    output_dict = dict_map(input_dict, value_func=lambda value: value ** 2)
    assert output_dict == {1: 1, 2: 4, 3: 9}

    output_dict = dict_map(input_dict, key_func=lambda key: key ** 2)
    assert output_dict == {1: 1, 4: 2, 9: 3}


@pytest.mark.parametrize(
    "before,after",
    [
        ({"test_key1": "test_value1"}, {"test_value1": ("test_key1",)}),
        (
            {
                "test_key1": "test_value1",
                "test_key2": "test_value2",
                "test_key3": "test_value1",
            },
            {"test_value1": ("test_key1", "test_key3"), "test_value2": ("test_key2",)},
        ),
        ({"a": {"b": "c"}}, {frozendict({"b": "c"}): ("a",)}),
        ({"a": frozendict({"b": "c"})}, {frozendict({"b": "c"}): ("a",)}),
        ({"a": {"b", "c"}}, {frozenset({"b", "c"}): ("a",)}),
        ({"a": frozenset({"b": "c"})}, {frozenset({"b": "c"}): ("a",)}),
        ({"a": ["b", "c"]}, {("b", "c"): ("a",)}),
        ({"a": ("b", "c")}, {("b", "c"): ("a",)}),
        # TODO: Use other unhashables, i.e. hypothesis non_hashable_strategies
    ],
)
def test_transpose_dict(before, after):
    assert transpose_dict(before) == after
