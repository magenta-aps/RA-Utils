from operator import attrgetter
from operator import itemgetter
from operator import getitem
from operator import setitem
from operator import delitem
from typing import Any

import hypothesis.strategies as st
from hypothesis import given

from ra_utils.attrdict import AttrDict
from .utils import any_strategy


def check_status_key(attr_dict: AttrDict, key: str, value: Any) -> None:
    assert attr_dict[key] == value
    assert getitem(attr_dict, key) == value
    assert getattr(attr_dict, key) == value
    assert itemgetter(key)(attr_dict) == value
    assert attrgetter(key)(attr_dict) == value
    assert attr_dict.__getitem__(key) == value
    assert attr_dict.__getattr__(key) == value


def check_status(attr_dict: AttrDict, value: Any) -> None:
    check_status_key(attr_dict, "status", value)
    assert attr_dict.status == value


@given(value=any_strategy)
def test_getattr_static(value):
    dicty = {"status": value}
    assert dicty["status"] == value
    assert getitem(dicty, "status") == value
    assert itemgetter("status")(dicty) == value

    attr_dict = AttrDict(dicty)
    check_status(attr_dict, value)


@given(value=any_strategy)
def test_setattr_static(value):
    dicty = {}
    dicty["status"] = value
    assert dicty["status"] == value

    attr_dict = AttrDict({})
    attr_dict["status"] = value
    check_status(attr_dict, value)

    attr_dict = AttrDict({})
    setitem(attr_dict, "status", value)
    check_status(attr_dict, value)

    attr_dict = AttrDict({})
    attr_dict.status = value
    check_status(attr_dict, value)

    attr_dict = AttrDict({})
    setattr(attr_dict, "status", value)
    check_status(attr_dict, value)


@given(value=any_strategy)
def test_delattr_static(value):
    dicty = {"status": value}
    del dicty["status"]
    assert dicty == {}
        
    attr_dict = AttrDict({"status": value})
    del attr_dict["status"]
    assert attr_dict == {}

    attr_dict = AttrDict({"status": value})
    delitem(attr_dict, "status")
    assert attr_dict == {}

    attr_dict = AttrDict({"status": value})
    del attr_dict.status
    assert attr_dict == {}

    attr_dict = AttrDict({"status": value})
    delattr(attr_dict, "status")
    assert attr_dict == {}


@given(key=st.text(min_size=2), value=any_strategy)
def test_getattr_static(key, value):
    dicty = {key: value}
    assert dicty[key] == value
    assert getitem(dicty, key) == value
    assert itemgetter(key)(dicty) == value

    attr_dict = AttrDict(dicty)
    check_status_key(attr_dict, key, value)


@given(key=st.text(min_size=2), value=any_strategy)
def test_setattr_static(key, value):
    dicty = {}
    dicty[key] = value
    assert dicty[key] == value

    attr_dict = AttrDict({})
    attr_dict[key] = value
    check_status_key(attr_dict, key, value)

    attr_dict = AttrDict({})
    setitem(attr_dict, key, value)
    check_status_key(attr_dict, key, value)

    attr_dict = AttrDict({})
    setattr(attr_dict, key, value)
    check_status_key(attr_dict, key, value)


@given(key=st.text(min_size=2), value=any_strategy)
def test_delattr_static(key, value):
    dicty = {key: value}
    del dicty[key]
    assert dicty == {}
        
    attr_dict = AttrDict({key: value})
    del attr_dict[key]
    assert attr_dict == {}

    attr_dict = AttrDict({key: value})
    delitem(attr_dict, key)
    assert attr_dict == {}

    attr_dict = AttrDict({key: value})
    delattr(attr_dict, key)
    assert attr_dict == {}
