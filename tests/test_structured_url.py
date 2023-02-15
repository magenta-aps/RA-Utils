# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Callable

import pytest

try:
    from pydantic import ValidationError

    from ra_utils.structured_url import StructuredUrl

    def skip_if_missing(func: Callable) -> Callable:
        return func

except:  # pragma: no cover  # noqa: E722
    StructuredUrl = object  # type: ignore

    skip_if_missing = pytest.mark.skipif(True, reason="pydantic not installed")


def _assert_parsed(structured_url: StructuredUrl) -> None:
    assert (
        structured_url.url
        == "https://username:password@example.com:1234/valid?a=b#here"
    )
    assert structured_url.url.scheme == "https"
    assert structured_url.scheme == "https"
    assert structured_url.url.user == "username"
    assert structured_url.user == "username"
    assert structured_url.url.password == "password"
    assert structured_url.password is not None
    assert structured_url.password.get_secret_value() == "password"
    assert structured_url.url.host == "example.com"
    assert structured_url.host == "example.com"
    assert structured_url.url.port == "1234"
    assert structured_url.port == 1234
    assert structured_url.url.path == "/valid"
    assert structured_url.path == "/valid"
    assert structured_url.url.query == "a=b"
    assert structured_url.query == {"a": "b"}
    assert structured_url.url.fragment == "here"
    assert structured_url.fragment == "here"


@skip_if_missing
def test_can_provide_url_directly() -> None:
    structured_url = StructuredUrl(
        url="https://username:password@example.com:1234/valid?a=b#here"
    )
    _assert_parsed(structured_url)


@skip_if_missing
def test_can_provide_url_indirectly() -> None:
    structured_url = StructuredUrl(
        scheme="https",
        user="username",
        password="password",
        host="example.com",
        port="1234",
        path="/valid",
        query={"a": "b"},
        fragment="here",
    )
    _assert_parsed(structured_url)


@skip_if_missing
def test_no_args_not_ok() -> None:
    with pytest.raises(ValidationError):
        StructuredUrl()
    with pytest.raises(ValidationError):
        StructuredUrl(scheme="http")
    StructuredUrl(scheme="http", host="a")


def _assert_parsed_minimal(structured_url: StructuredUrl) -> None:
    assert structured_url.url == "http://a"
    assert structured_url.url.scheme == "http"
    assert structured_url.scheme == "http"
    assert structured_url.url.host == "a"
    assert structured_url.host == "a"
    assert structured_url.query == {}

    none_fields = {"user", "password", "port", "path", "fragment"}
    for key in none_fields:
        assert getattr(structured_url.url, key) is None
        assert getattr(structured_url, key) is None


@skip_if_missing
def test_minimal_url_directly_ok() -> None:
    structured_url = StructuredUrl(url="http://a")
    _assert_parsed_minimal(structured_url)


@skip_if_missing
def test_minimal_url_indirectly_ok() -> None:
    structured_url = StructuredUrl(scheme="http", host="a")
    _assert_parsed_minimal(structured_url)


@skip_if_missing
def test_url_is_conflicts_with_others() -> None:
    # Conflicting information here, url always wins
    with pytest.raises(ValidationError):
        StructuredUrl(url="https://b", scheme="http", host="a")


@skip_if_missing
@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://username:password@example.com/mypath#here?now=1",
        "postgresql://username:password@db/mydb",
        "postgresql+asyncpg://username:password@db/mydb",
    ],
)
def test_that_urls_are_ok(url: str) -> None:
    StructuredUrl(url=url)


@skip_if_missing
@pytest.mark.parametrize(
    "url",
    [
        "sqlite+aiosqlite:///:memory:",
        "sqlite:///db.sqlite3",
        "sqlite+aiosqlite:///db.sqlite3",
        "sqlite:////C:/db.sqlite3",
        "sqlite+aiosqlite:////tmp/db.sqlite3",
    ],
)
def test_that_urls_are_rejected(url: str) -> None:
    with pytest.raises(ValidationError):
        StructuredUrl(url=url)
