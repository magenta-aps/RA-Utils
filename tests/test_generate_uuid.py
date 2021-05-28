#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from unittest import TestCase
from uuid import UUID

from hypothesis import given
from hypothesis.strategies import text

from ra_utils.generate_uuid import _generate_uuid
from ra_utils.generate_uuid import generate_uuid
from ra_utils.generate_uuid import uuid_generator


class test_generate_uuid(TestCase):
    @given(text(), text())
    def test_generate_uuid(self, base, value):
        uuid1 = generate_uuid(base, value)
        _generate_uuid.cache_clear()
        uuid2 = generate_uuid(base, value)
        _generate_uuid.cache_clear()
        uuid3 = generate_uuid(base, value + "A different string")
        assert uuid1 == uuid2
        assert uuid1 != uuid3
        assert isinstance(uuid1, UUID)

    @given(text(), text())
    def test_create_generator(self, base, value):
        gen = uuid_generator(base)
        uuid1 = gen(value)
        uuid2 = gen(value)
        assert uuid1 == uuid2
        assert uuid_generator(value) != gen(value + "Another string")
        assert isinstance(uuid1, UUID)

    @given(text(), text())
    def test_generator_output(self, base, value):
        assert generate_uuid(base, value) == uuid_generator(base)(value)
