#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import hypothesis.strategies as st
import pytest
from hypothesis import given

from ra_utils.wraps import wraps_and_append_kwargs


def foo(a, b):
    return a + b


@wraps_and_append_kwargs(foo)
def bar(*args, c, **kwargs):
    return foo(*args, **kwargs) * c


@wraps_and_append_kwargs(foo)
def qux(*args, c=None, **kwargs):
    return (args, c, kwargs)


class Corge:
    def fez(self, a, b):
        return a + b

    @wraps_and_append_kwargs(fez)
    def barz(self, *args, c, **kwargs):
        return self.fez(*args, **kwargs) * c

    @wraps_and_append_kwargs(foo)
    def barf(self, *args, c, **kwargs):
        return foo(*args, **kwargs) * c

    @wraps_and_append_kwargs(fez)
    def quxz(self, *args, c=None, **kwargs):
        return (self, args, c, kwargs)

    @wraps_and_append_kwargs(foo)
    def quxf(self, *args, c=None, **kwargs):
        return (self, args, c, kwargs)


@given(st.integers(), st.integers(), st.integers())
def test_all_ok(a, b, c):
    expected_result = (a + b) * c

    d = Corge()

    assert bar(a, b, c=c) == expected_result
    assert d.barz(a, b, c=c) == expected_result
    assert d.barf(a, b, c=c) == expected_result

    assert qux(a, b, c=c) == ((a, b), c, {})
    assert d.quxz(a, b, c=c) == (d, (a, b), c, {})
    assert d.quxf(a, b, c=c) == (d, (a, b), c, {})

    assert bar(a, b=b, c=c) == expected_result
    assert d.barz(a, b=b, c=c) == expected_result
    assert d.barf(a, b=b, c=c) == expected_result

    assert qux(a, b=b, c=c) == ((a,), c, {"b": b})
    assert d.quxz(a, b=b, c=c) == (d, (a,), c, {"b": b})
    assert d.quxf(a, b=b, c=c) == (d, (a,), c, {"b": b})

    assert bar(a=a, b=b, c=c) == expected_result
    assert d.barz(a=a, b=b, c=c) == expected_result
    assert d.barf(a=a, b=b, c=c) == expected_result

    assert qux(a=a, b=b, c=c) == (tuple(), c, {"a": a, "b": b})
    assert d.quxz(a=a, b=b, c=c) == (d, tuple(), c, {"a": a, "b": b})
    assert d.quxf(a=a, b=b, c=c) == (d, tuple(), c, {"a": a, "b": b})

    assert bar(c=c, b=b, a=a) == expected_result
    assert d.barz(c=c, b=b, a=a) == expected_result
    assert d.barf(c=c, b=b, a=a) == expected_result

    assert qux(c=c, b=b, a=a) == (tuple(), c, {"a": a, "b": b})
    assert d.quxz(c=c, b=b, a=a) == (d, tuple(), c, {"a": a, "b": b})
    assert d.quxf(c=c, b=b, a=a) == (d, tuple(), c, {"a": a, "b": b})

    with pytest.raises(TypeError) as excinfo:
        bar(a, b, c)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barz(a, b, c)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barf(a, b, c)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)

    assert qux(a, b, c) == ((a, b, c), None, {})
    assert d.quxz(a, b, c) == (d, (a, b, c), None, {})
    assert d.quxf(a, b, c) == (d, (a, b, c), None, {})

    with pytest.raises(TypeError) as excinfo:
        bar(a, b)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barz(a, b)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barf(a, b)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)

    assert qux(a, b) == ((a, b), None, {})
    assert d.quxz(a, b) == (d, (a, b), None, {})
    assert d.quxf(a, b) == (d, (a, b), None, {})

    with pytest.raises(TypeError) as excinfo:
        bar(a)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barz(a)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        d.barf(a)
    assert "missing 1 required keyword-only argument: 'c'" in str(excinfo.value)

    assert qux(a) == ((a,), None, {})
    assert d.quxz(a) == (d, (a,), None, {})
    assert d.quxf(a) == (d, (a,), None, {})


def test_non_kwarg():
    def baz(c, *args, **kwargs):
        return foo(*args, **kwargs)

    with pytest.raises(AssertionError) as excinfo:
        wraps_and_append_kwargs(foo)(baz)
    assert "'wraps_and_append_kwargs' only support pure keywork arguments" in str(
        excinfo.value
    )
