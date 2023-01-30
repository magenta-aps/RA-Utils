# SPDX-FileCopyrightText: 2022 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
"""Pydantic StructuredUrl model."""
from functools import wraps
from typing import Any
from typing import Callable
from typing import cast
from typing import TypeVar
from urllib.parse import parse_qsl
from urllib.parse import urlencode

try:
    from pydantic import AnyUrl
    from pydantic import BaseModel
    from pydantic import Field
    from pydantic import SecretStr
    from pydantic import parse_obj_as
    from pydantic import root_validator
except ImportError as err:  # pragma: no cover
    raise ImportError(f"{err.name} not found - {__name__} not imported")


T = TypeVar("T")
R = TypeVar("R")


def none_early_return(func: Callable[[T], R]) -> Callable[[T | None], R | None]:
    """Decorate a function to early return 'None' on 'None'."""

    @wraps(func)
    def wrapper(arg: T | None) -> R | None:
        return func(arg) if arg is not None else None

    return wrapper


opt_int2str = none_early_return(str)
opt_str2int = none_early_return(int)

opt_urldecode = none_early_return(
    cast(Callable[[str], dict], lambda qs: dict(parse_qsl(qs)))
)
opt_urlencode = none_early_return(urlencode)


# pylint: disable=too-few-public-methods
class StructuredUrl(BaseModel):
    """Structured Url object.

    Allows for constructing a url either directly or indirectly."""

    class Config:
        """Settings are frozen."""

        frozen = True

    url: AnyUrl = Field(..., description="Database URL.")

    scheme: str | None
    user: str | None
    password: SecretStr | None
    host: str | None
    port: int | None
    path: str | None
    query: dict[str, str] | None
    fragment: str | None

    @root_validator(pre=True)
    def ensure_url(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure that url is set.

        Args:
            values: Pydantic parsed values.

        Returns:
            'values' but with the guarantee that 'url' is set.
        """
        # If 'url' is set, noop.
        if values.get("url"):
            if len(values) != 1:
                raise ValueError("cannot provide both url and structured fields")
            return values

        if "scheme" not in values:
            raise ValueError("scheme is required")
        if "host" not in values:
            raise ValueError("host is required")

        uri_string = AnyUrl.build(
            scheme=values.get("scheme"),
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=opt_int2str(values.get("port")),
            path=values.get("path"),
            query=opt_urlencode(values.get("query")),
            fragment=values.get("fragment"),
        )
        values["url"] = parse_obj_as(AnyUrl, uri_string)
        return values

    @root_validator(pre=True)
    def ensure_xstructured_fields(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Ensure that our structured fields are set.

        Args:
            values: Pydantic parsed values.

        Returns:
            'values' but with the guarantee that all non-'url' fields are set.
        """
        # If 'url' is not set at this point, error out.
        assert values["url"] is not None

        url = parse_obj_as(AnyUrl, values["url"])
        values.update(
            dict(
                scheme=url.scheme,
                user=url.user,
                password=url.password,
                host=url.host,
                port=opt_str2int(url.port),
                path=url.path,
                query=opt_urldecode(url.query),
                fragment=url.fragment,
            )
        )
        return values
