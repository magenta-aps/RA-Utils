#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import os

from hypothesis import settings


settings.register_profile("ci", max_examples=1000)
settings.load_profile(os.getenv(u"HYPOTHESIS_PROFILE", "default"))
