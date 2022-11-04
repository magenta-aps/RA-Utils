# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import logging
import sys
from enum import auto
from enum import Enum
from typing import Any
from typing import Dict
from typing import Tuple

from pydantic import BaseSettings
from pydantic import Extra
from pydantic.env_settings import SettingsSourceCallable

from .load_settings import load_settings


logger = logging.getLogger(__name__)


def _get_json_settings_source(prefix: str) -> SettingsSourceCallable:
    """Create a Pydantic settings source which reads the DIPEX `settings.json`

    Args:
        prefix (str): Retrieve only the settings in `settings.json` whose key match this
                      prefix.
    """

    def settings_source(base_settings: BaseSettings) -> Dict[str, Any]:
        # The actual settings source callable

        try:
            all_settings = load_settings()
        except FileNotFoundError:
            # `print()` is used instead of `logger.warning()` here, as logging is
            # probably not yet configured at this point.
            print("Could not load 'settings.json', using settings from environment")
            return {}

        # Retrieve all settings matching `prefix`, and convert dots in setting keys to
        # underscores, so they become valid setting names for Pydantic settings.
        settings: Dict[str, Any] = {
            key.replace(".", "_"): val
            for key, val in all_settings.items()
            if key.startswith(prefix)
        }

        # Add log level to settings, if defined
        if "log_level" in all_settings:
            settings["log_level"] = all_settings["log_level"]

        return settings

    return settings_source


class LogLevel(Enum):
    """Represent log levels of the Python `logging` library as an `Enum`.

    This allows us to read the desired log level in `IntegrationSettings`  without
    additional parsing or conversion.
    """

    def _generate_next_value_(name, start, count, last_values):  # type: ignore
        # Generate enum elements whose key and values are identical.
        # See: https://docs.python.org/3.9/library/enum.html#using-automatic-values
        # Must be defined *before* the enum elements to work correctly.
        return name

    NOTSET = auto()
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class JobSettings(BaseSettings):
    """Base class for defining the settings of a given OS2MO integration job.

    Each integration should define its settings like this:
    >>> class SqlExportSettings(JobSettings):
    >>>
    >>>     class Config:
    >>>         # Optional: Only use settings from settings.json if they match this
    >>>         # prefix.
    >>>         settings_json_prefix = "exporters.actual_state"

    And then read its settings like this:
    >>> settings = SqlExportSettings()

    And configure logging according to the settings like this:
    >>> settings.start_logging_based_on_settings()
    """

    log_level: LogLevel = LogLevel.ERROR
    log_format: str = (
        "%(levelname)s %(asctime)s %(filename)s:%(lineno)d:%(name)s: %(message)s"
    )

    class Config:
        # Configuration attributes defined by the Pydantic `Config` class
        extra: Extra = Extra.allow
        env_file_encoding: str = "utf-8"
        use_enum_values: bool = True

        # Additional configuration attributes defined by us.
        settings_json_prefix: str = ""

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            """Add settings source which reads settings from 'settings.json'"""
            json_settings = _get_json_settings_source(cls.settings_json_prefix)
            return (
                init_settings,
                env_settings,
                json_settings,
                file_secret_settings,
            )

    def start_logging_based_on_settings(self) -> None:
        """Configure Python `logging` library according to these integration settings"""
        # Based on https://stackoverflow.com/a/14058475

        # Get root logger and set its log level
        root: logging.Logger = logging.getLogger()
        root.setLevel(self.log_level)  # type: ignore

        # Create handler logging to stdout, and set its log level
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)  # type: ignore

        # Set the log format of the handler
        formatter: logging.Formatter = logging.Formatter(self.log_format)
        handler.setFormatter(formatter)

        # Add the handler logging to stdout to the root logger
        root.addHandler(handler)