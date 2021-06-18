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

from .utils import any_strategy
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


@given(value=any_strategy)
def test_getattr_static(value):
    dicty = {"status": value}
    assert dicty["status"] == value
    assert getitem(dicty, "status") == value
    assert itemgetter("status")(dicty) == value

    frozen_dict = frozendict(**dicty)
    check_status(frozen_dict, value)


@given(value=any_strategy)
def test_setattr_static(value):
    dicty = {}
    dicty["status"] = value
    assert dicty["status"] == value

    frozen_dict = frozendict({})
    with pytest.raises(TypeError) as exc_info:
        frozen_dict["status"] = value  # type: ignore
    assert no_assignment_error in str(exc_info.value)

    frozen_dict = frozendict({})
    with pytest.raises(TypeError) as exc_info:
        setitem(frozen_dict, "status", value)  # type: ignore
    assert no_assignment_error in str(exc_info.value)


@given(value=any_strategy)
def test_delattr_static(value):
    dicty = {"status": value}
    del dicty["status"]
    assert dicty == {}

    frozen_dict = frozendict({"status": value})
    with pytest.raises(TypeError) as exc_info:
        del frozen_dict["status"]  # type: ignore
    assert no_deletion_error in str(exc_info.value)

    frozen_dict = frozendict({"status": value})
    with pytest.raises(TypeError) as exc_info:
        delitem(frozen_dict, "status")  # type: ignore
    assert no_deletion_error in str(exc_info.value)


@given(key=st.text(min_size=1), value=any_strategy)
def test_getattr_dynamic(key, value):
    dicty = {key: value}
    assert dicty[key] == value
    assert getitem(dicty, key) == value
    assert itemgetter(key)(dicty) == value

    frozen_dict = frozendict(dicty)
    check_status_key(frozen_dict, key, value)


@given(key=st.text(min_size=1), value=any_strategy)
def test_setattr_dynamic(key, value):
    dicty = {}
    dicty[key] = value
    assert dicty[key] == value

    frozen_dict = frozendict({})
    with pytest.raises(TypeError) as exc_info:
        frozen_dict[key] = value  # type: ignore
    assert no_assignment_error in str(exc_info.value)

    frozen_dict = frozendict({})
    with pytest.raises(TypeError) as exc_info:
        setitem(frozen_dict, key, value)  # type: ignore
    assert no_assignment_error in str(exc_info.value)


@given(key=st.text(min_size=1), value=any_strategy)
def test_delattr_dynamic(key, value):
    dicty = {key: value}
    del dicty[key]
    assert dicty == {}

    frozen_dict = frozendict({key: value})
    with pytest.raises(TypeError) as exc_info:
        del frozen_dict[key]  # type: ignore
    assert no_deletion_error in str(exc_info.value)

    frozen_dict = frozendict({key: value})
    with pytest.raises(TypeError) as exc_info:
        delitem(frozen_dict, key)  # type: ignore
    assert no_deletion_error in str(exc_info.value)
