#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import re
from functools import lru_cache
from typing import Pattern

# --------------------------------------------------------------------------------------
# Strategies
# --------------------------------------------------------------------------------------

try:
    from hypothesis import strategies as st
except ImportError:  # pragma: no cover
    raise ImportError("hypothesis not found - strategies not imported")


def not_from_regex(str_pat: str) -> st.SearchStrategy:
    @lru_cache
    def cached_regex(str_pat: str) -> Pattern:
        return re.compile(str_pat)

    regex = cached_regex(str_pat)
    return st.text().filter(lambda s: regex.match(s) is None)
