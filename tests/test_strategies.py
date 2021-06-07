#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from hypothesis import given
from hypothesis import strategies as st

from ra_utils.strategies import not_from_regex

# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------


@given(not_string=not_from_regex(r"test"), string=st.from_regex(r"test"))
def test_strategy(not_string, string):
    assert not_string != string
