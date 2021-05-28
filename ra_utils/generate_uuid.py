#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import hashlib
from functools import lru_cache
from functools import partial
from typing import Callable
from uuid import UUID


@lru_cache(maxsize=None)
def _generate_uuid(value: str) -> UUID:
    value_hash = hashlib.md5(value.encode())
    value_digest = value_hash.hexdigest()
    return UUID(value_digest)


def generate_uuid(base: str, value: str) -> UUID:
    """
    Generate a predictable uuid based on org name and a unique value.
    """
    base_uuid = _generate_uuid(base)
    return _generate_uuid(str(base_uuid) + str(value))


def uuid_generator(base: str) -> Callable[[str], UUID]:
    """Make an UUID generator with a fixed base/seed.

    Example:
        uuid_gen = uuid_generator("secret_seed")
        uuid1 = uuid_gen("facetnavn1")
        uuid2 = uuid_gen("facetnavn1")
        uuid3 = uuid_gen("facetnavn2")
        assert uuid1 == uuid2
        assert uuid1 != uuid3

    Args:
        base (str): Base/seed utilized for all calls to generator.

    Returns:
        Callable: Function to map strings to UUIDs.
    """
    return partial(generate_uuid, base)
