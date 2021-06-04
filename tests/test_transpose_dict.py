#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import pytest

from ra_utils.transpose_dict import transpose_dict


@pytest.mark.parametrize(
    "before,after",
    [
        (
            {'test_key1': 'test_value1'},
            {'test_value1': ['test_key1']}
        ),
        (
            { 
                'test_key1': 'test_value1', 
                'test_key2': 'test_value2', 
                'test_key3': 'test_value1'
            },
            {
                'test_value1': ['test_key1', 'test_key3'],
                'test_value2': ['test_key2']
            } 
        )
    ],
)
def test_transpose_dict(before, after):
    assert transpose_dict(before) == after
