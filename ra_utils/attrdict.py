#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------


class AttrDict(dict):
    """Enable dot.notation access for a dict object.

    Example:
        script_result = AttrDict({"exit_code": 0})
        self.assertEqual(script_result.exit_code, 0)
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__  # type: ignore
    __delattr__ = dict.__delitem__  # type: ignore
