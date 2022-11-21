# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import logging
from typing import Any
from typing import ContextManager
from unittest.mock import patch
from uuid import uuid4

import pytest

from ra_utils.job_settings import JobSettings
from ra_utils.job_settings import LogLevel


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("CLIENT_SECRET", str(uuid4()))


class _ExampleSettings(JobSettings):
    pass


class _ExamplePrefixSettings(_ExampleSettings):
    class Config:
        settings_json_prefix: str = "a."


def _mock_settings(**kwargs: Any) -> ContextManager:
    return patch("ra_utils.job_settings.load_settings", **kwargs)


def test_log_level_uses_default(mock_env):
    with _mock_settings(return_value={}):
        settings: _ExampleSettings = _ExampleSettings()
        assert settings.log_level == LogLevel.ERROR.value  # the default is ERROR


def test_json_settings_source_handles_file_not_found(mock_env):
    with _mock_settings(side_effect=FileNotFoundError):
        settings: _ExampleSettings = _ExampleSettings()
        assert settings.log_level == LogLevel.ERROR.value  # the default is ERROR


def test_log_level_uses_settings_json_value(mock_env):
    with _mock_settings(return_value={"log_level": "INFO"}):
        settings: _ExampleSettings = _ExampleSettings()
        assert settings.log_level == LogLevel.INFO.value


def test_json_settings_source_filters_on_prefix(mock_env):
    with _mock_settings(return_value={"a.a": "a", "b.b": "b"}):
        settings: _ExamplePrefixSettings = _ExamplePrefixSettings()
        assert settings.a_a == "a"  # type: ignore
        assert "b_b" not in settings.dict()


def test_start_logging_based_on_settings(caplog, mock_env):
    # Arrange
    logger = logging.getLogger(__name__)
    with _mock_settings(return_value={}):
        settings: _ExampleSettings = _ExampleSettings()
        # Act: set up logging and make logging calls
        settings.start_logging_based_on_settings()
        logger.info("info")
        logger.error("error")

    # Assert: only ERROR log lines are present, since the default log level is ERROR
    assert "error" in caplog.text
    assert "info" not in caplog.text
