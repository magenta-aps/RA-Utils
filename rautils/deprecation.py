#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import warnings
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional


def deprecated(func: Callable) -> Callable:
    """Mark the decorated function as deprecated."""

    @wraps(func)
    def new_func(*args: Any, **kwargs: Optional[Any]) -> Any:
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return new_func
