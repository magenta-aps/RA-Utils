#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from operator import delitem
from operator import getitem
from operator import itemgetter
from operator import setitem
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from .utils import recursive_strategies
from ra_utils.ensure_hashable import ensure_hashable
from ra_utils.frozen_dict import FrozenDict
from ra_utils.frozen_dict import frozendict

no_assignment_error = "'FrozenDict' object does not support item assignment"
no_deletion_error = "'FrozenDict' object does not support item deletion"


def check_status_key(frozen_dict: FrozenDict, key: str, value: Any) -> None:
    assert frozen_dict[key] == value
    assert getitem(frozen_dict, key) == value
    assert itemgetter(key)(frozen_dict) == value
    assert frozen_dict.__getitem__(key) == value


def check_status(frozen_dict: FrozenDict, value: Any) -> None:
    check_status_key(frozen_dict, "status", value)


@given(value=st.one_of(recursive_strategies))
def test_getitem_static(value):
    dicty = {"status": value}
    assert dicty["status"] == value
    assert getitem(dicty, "status") == value
    assert itemgetter("status")(dicty) == value

    frozen_dict = frozendict(status=value)
    check_status(frozen_dict, value)


@given(value=st.one_of(recursive_strategies))
def test_setitem_static(value):
    dicty = {}
    dicty["status"] = value
    assert dicty["status"] == value

    frozen_dict = frozendict()
    with pytest.raises(TypeError) as exc_info:
        frozen_dict["status"] = value  # type: ignore
    assert no_assignment_error in str(exc_info.value)

    frozen_dict = frozendict()
    with pytest.raises(TypeError) as exc_info:
        setitem(frozen_dict, "status", value)  # type: ignore
    assert no_assignment_error in str(exc_info.value)


@given(value=st.one_of(recursive_strategies))
def test_delitem_static(value):
    dicty = {"status": value}
    del dicty["status"]
    assert dicty == {}

    frozen_dict = frozendict(status=value)
    with pytest.raises(TypeError) as exc_info:
        del frozen_dict["status"]  # type: ignore
    assert no_deletion_error in str(exc_info.value)

    frozen_dict = frozendict(status=value)
    with pytest.raises(TypeError) as exc_info:
        delitem(frozen_dict, "status")  # type: ignore
    assert no_deletion_error in str(exc_info.value)


@given(key=st.text(min_size=1), value=st.one_of(recursive_strategies))
def test_getitem_dynamic(key, value):
    dicty = {key: value}
    assert dicty[key] == value
    assert getitem(dicty, key) == value
    assert itemgetter(key)(dicty) == value

    frozen_dict = frozendict(**dicty)
    check_status_key(frozen_dict, key, value)


@given(key=st.text(min_size=1), value=st.one_of(recursive_strategies))
def test_setitem_dynamic(key, value):
    dicty = {}
    dicty[key] = value
    assert dicty[key] == value

    frozen_dict = frozendict()
    with pytest.raises(TypeError) as exc_info:
        frozen_dict[key] = value  # type: ignore
    assert no_assignment_error in str(exc_info.value)

    frozen_dict = frozendict()
    with pytest.raises(TypeError) as exc_info:
        setitem(frozen_dict, key, value)  # type: ignore
    assert no_assignment_error in str(exc_info.value)


@given(key=st.text(min_size=1), value=st.one_of(recursive_strategies))
def test_delitem_dynamic(key, value):
    dicty = {key: value}
    del dicty[key]
    assert dicty == {}

    frozen_dict = frozendict(**{key: value})
    with pytest.raises(TypeError) as exc_info:
        del frozen_dict[key]  # type: ignore
    assert no_deletion_error in str(exc_info.value)

    frozen_dict = frozendict(**{key: value})
    with pytest.raises(TypeError) as exc_info:
        delitem(frozen_dict, key)  # type: ignore
    assert no_deletion_error in str(exc_info.value)


@given(st.dictionaries(st.text(), st.text()))
def test_ordinary_dict_functionality(dicty: dict):
    """Test that FrozenDict functions similar to an ordinary dict."""
    frozen_dict = frozendict(**dicty)

    assert dicty.items() == frozen_dict.items()
    assert len(dicty) == len(frozen_dict)
    assert str(dicty) == str(frozen_dict)
    assert repr(dicty) == repr(frozen_dict)

    for key in dicty.keys():
        assert dicty[key] == frozen_dict[key]


@given(st.dictionaries(st.text(), st.text()))
def test_hash(dicty: dict):
    with pytest.raises(TypeError) as exc_info:
        hash(dicty)
    assert "unhashable type: 'dict'" in str(exc_info.value)

    hashval1 = hash(frozendict(**dicty))
    hashval2 = hash(frozendict(**dicty))
    assert hashval1 == hashval2


def test_hash_emptydict():
    assert hash(frozendict()) == 0
    assert hash(frozendict()) == 0


def test_hash_tuples():
    dicty = ensure_hashable({"a": 1, None: None, b"": 3, "": {}})
    hashval1 = hash(dicty)
    hashval2 = hash(dicty)
    assert hashval1 == hashval2

    dicty = ensure_hashable(
        {"a": None, "b": {"c": "d"}, "e": ["f", "g"], "h": {"i", "j"}}
    )
    hashval1 = hash(dicty)
    hashval2 = hash(dicty)
    assert hashval1 == hashval2


def test_constructors():
    a = frozendict({'a': 1})
    assert a['a'] == 1
    b = frozendict([('a', 1)])
    assert b['a'] == 1
    c = frozendict(iter([('a', 1)]))
    assert c['a'] == 1
    d = frozendict(a=1)
    assert d['a'] == 1

    with pytest.raises(TypeError) as exc_info:
        frozendict(1)
    assert "<class 'int'> object is not iterable" in str(exc_info.value)
