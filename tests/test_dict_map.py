#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from functools import partial
from typing import Dict

import pytest
from hypothesis import assume
from hypothesis import given
from hypothesis import strategies as st

from ra_utils.transpose_dict import dict_map


def swapcase(x):
    return x.swapcase()


def pow2(x):
    return x ** 2


@pytest.mark.parametrize(
    "dict_map_func",
    [
        dict_map,
        partial(dict_map, key_func=swapcase),
        partial(dict_map, value_func=swapcase),
        partial(dict_map, key_func=swapcase, value_func=swapcase),
    ],
)
def test_dictmap_identity(dict_map_func):
    dicty: Dict[str, str] = {}
    mapped = dict_map_func(dicty)
    assert id(mapped) == id(dicty)
    assert dicty == {}


@given(st.dictionaries(st.text(), st.text(), min_size=1))
def test_dictmap_swapcase(dicty):
    mapped = dict_map(dicty)
    assert id(mapped) == id(dicty)
    assert dict_map(mapped) == dicty

    mapped = dict_map(
        dicty,
        key_func=swapcase,
    )
    assert id(mapped) != id(dicty)
    assert sorted(mapped.keys()) == sorted(map(swapcase, dicty.keys()))
    assert sorted(mapped.values()) == sorted(dicty.values())

    mapped = dict_map(
        dicty,
        value_func=swapcase,
    )
    assert id(mapped) != id(dicty)
    assert sorted(mapped.keys()) == sorted(dicty.keys())
    assert sorted(mapped.values()) == sorted(map(swapcase, dicty.values()))

    mapped = dict_map(
        dicty,
        key_func=swapcase,
        value_func=swapcase,
    )
    assert id(mapped) != id(dicty)
    assert sorted(mapped.keys()) == sorted(map(swapcase, dicty.keys()))
    assert sorted(mapped.values()) == sorted(map(swapcase, dicty.values()))


@given(st.dictionaries(st.text(), st.integers(), min_size=1))
def test_dictmap_pow2(dicty):
    mapped = dict_map(
        dicty,
        key_func=swapcase,
        value_func=pow2,
    )
    assert id(mapped) != id(dicty)
    assert sorted(mapped.keys()) == sorted(map(swapcase, dicty.keys()))
    assert sorted(mapped.values()) == sorted(map(pow2, dicty.values()))


@given(st.dictionaries(st.text(), st.text(), min_size=1))
def test_dictmap_invalid_operation(dicty):
    with pytest.raises(TypeError) as exc_info:
        dict_map(
            dicty,
            key_func=pow2,
        )
    assert "unsupported operand type(s) for ** or pow():" in str(exc_info.value)


@given(st.text(min_size=1))
def test_dict_map_destructive_key_interference(key):
    # Any non-bijective function would work here
    def to_upper(x):
        return x.upper()

    assume(key != to_upper(key))

    dicty = {key: 0, to_upper(key): 1}
    mapped = dict_map(
        dicty,
        key_func=to_upper,
    )
    assert id(mapped) != id(dicty)
    assert len(mapped.keys()) == 1
    assert len(mapped.values()) == 1
    assert len(dicty.keys()) == 2
    assert len(dicty.values()) == 2
