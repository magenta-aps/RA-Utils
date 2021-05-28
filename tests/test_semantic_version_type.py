#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from contextlib import suppress as do_not_raise
from typing import Any

import pytest

from ra_utils.semantic_version_type import _has_pydantic
from ra_utils.semantic_version_type import get_regex
from ra_utils.semantic_version_type import SemanticVersion
from ra_utils.semantic_version_type import SemanticVersionModel


@pytest.mark.parametrize(
    "version,valid",
    [
        # Valid
        ("0.0.4", True),
        ("1.2.3", True),
        ("10.20.30", True),
        ("1.1.2-prerelease+meta", True),
        ("1.1.2+meta", True),
        ("1.1.2+meta-valid", True),
        ("1.0.0-alpha", True),
        ("1.0.0-beta", True),
        ("1.0.0-alpha.beta", True),
        ("1.0.0-alpha.beta.1", True),
        ("1.0.0-alpha.1", True),
        ("1.0.0-alpha0.valid", True),
        ("1.0.0-alpha.0valid", True),
        ("1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay", True),
        ("1.0.0-rc.1+build.1", True),
        ("2.0.0-rc.1+build.123", True),
        ("1.2.3-beta", True),
        ("10.2.3-DEV-SNAPSHOT", True),
        ("1.2.3-SNAPSHOT-123", True),
        ("1.0.0", True),
        ("2.0.0", True),
        ("1.1.7", True),
        ("2.0.0+build.1848", True),
        ("2.0.1-alpha.1227", True),
        ("1.0.0-alpha+beta", True),
        ("1.2.3----RC-SNAPSHOT.12.9.1--.12+788", True),
        ("1.2.3----R-S.12.9.1--.12+meta", True),
        ("1.2.3----RC-SNAPSHOT.12.9.1--.12", True),
        ("1.0.0+0.build.1-rc.10000aaa-kk-0.1", True),
        ("99999999999999999999999.999999999999999999.99999999999999999", True),
        ("1.0.0-0A.is.legal", True),
        # Invalid
        ("1", False),
        ("1.2", False),
        ("1.2.3-0123", False),
        ("1.2.3-0123.0123", False),
        ("1.1.2+.123", False),
        ("+invalid", False),
        ("-invalid", False),
        ("-invalid+invalid", False),
        ("-invalid.01", False),
        ("alpha", False),
        ("alpha.beta", False),
        ("alpha.beta.1", False),
        ("alpha.1", False),
        ("alpha+beta", False),
        ("alpha_beta", False),
        ("alpha.", False),
        ("alpha..", False),
        ("beta", False),
        ("1.0.0-alpha_beta", False),
        ("-alpha.", False),
        ("1.0.0-alpha..", False),
        ("1.0.0-alpha..1", False),
        ("1.0.0-alpha...1", False),
        ("1.0.0-alpha....1", False),
        ("1.0.0-alpha.....1", False),
        ("1.0.0-alpha......1", False),
        ("1.0.0-alpha.......1", False),
        ("01.1.1", False),
        ("1.01.1", False),
        ("1.1.01", False),
        ("1.2", False),
        ("1.2.3.DEV", False),
        ("1.2-SNAPSHOT", False),
        ("1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788", False),
        ("1.2-RC-SNAPSHOT", False),
        ("-1.0.3-gamma+b7718", False),
        ("+justmeta", False),
        ("9.8.7+meta+meta", False),
        ("9.8.7-whatever+meta+meta", False),
        ("9.9.9----RC-SNAPSHOT.12.09.1------..12", False),
    ],
)
@pytest.mark.skipif(_has_pydantic is False, reason="pydantic not installed")
def test_semantic_version_validity(version: str, valid: bool):
    from pydantic import ValidationError

    # Check regex itself
    regex = get_regex()
    matches = bool(regex.match(version))
    assert matches == valid

    # Check fieldtype
    field_context_manager: Any = do_not_raise()
    if not valid:
        field_context_manager = pytest.raises(ValueError)

    with field_context_manager:
        semantic_version = SemanticVersion()
        semantic_version.validate(version)

    # Check model
    model_context_manager: Any = do_not_raise()
    if not valid:
        model_context_manager = pytest.raises(ValidationError)

    with model_context_manager:
        SemanticVersionModel(__root__=version)
