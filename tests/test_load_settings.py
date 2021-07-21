#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from unittest import TestCase
from unittest.mock import mock_open
from unittest.mock import patch

from ra_utils.load_settings import load_setting
from ra_utils.load_settings import load_settings


class LoadSettingsTests(TestCase):
    def setUp(self):
        # Clear the lru_cache in between tests
        load_settings.cache_clear()

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_cache(self, mock_file):
        """Test that calling load_settings multiple times only reads the file once.

        The test only tries twice, but could do it 'n' times.
        """
        result1 = load_settings()
        result2 = load_settings()
        mock_file.assert_called_once()
        self.assertEqual(result1, result2)

    @patch("builtins.open", new_callable=mock_open, read_data='{"a": 1}')
    def test_load_one_setting(self, mock_file):
        result1 = load_setting("a")()
        self.assertEqual(result1, 1)

        result2 = load_setting("a", 2)()
        self.assertEqual(result2, 1)

        result3 = load_setting("b", 3)()
        self.assertEqual(result3, 3)

        with self.assertRaises(ValueError):
            load_setting("b")()

        mock_file.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_missing_file(self, mock_file):
        """Test that load_settings propergates FileNotFound errors."""
        mock_file.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            load_settings()
