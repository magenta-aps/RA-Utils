#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import time
from datetime import timedelta

import pytest
import requests
from hypothesis import example
from hypothesis import given
from hypothesis import strategies as st
from pytest import MonkeyPatch

# --------------------------------------------------------------------------------------
# Check if we should skip
# --------------------------------------------------------------------------------------

no_deps = False
try:
    from ra_utils.headers import AuthError
    from ra_utils.headers import TokenSettings
except ImportError:
    no_deps = True

pytestmark = pytest.mark.skipif(no_deps, reason="Header dependencies not installed")


# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


class MockResponse:
    def __init__(self, response_dict, raise_msg="") -> None:
        self.response = response_dict
        self.raise_msg = raise_msg

    def json(self):
        return self.response

    def raise_for_status(self):
        if self.raise_msg:
            raise requests.RequestException(self.raise_msg)
        else:
            pass


def test_init(monkeypatch):
    monkeypatch.setenv("SAML_TOKEN", "test token")
    with pytest.deprecated_call():
        assert TokenSettings()
    monkeypatch.delenv("SAML_TOKEN", raising=False)
    monkeypatch.setenv("CLIENT_SECRET", "test secret")
    assert TokenSettings()


def test_validation(monkeypatch):
    # delete token/secret if they exist
    monkeypatch.delenv("SAML_TOKEN", raising=False)
    monkeypatch.delenv("CLIENT_SECRET", raising=False)
    with pytest.warns(UserWarning, match="No secret or token given"):
        TokenSettings()


@given(t_delta=st.timedeltas())
def test_fetch_keycloak(t_delta: timedelta):
    def mock_post(*args, **kwargs):
        return MockResponse(
            {"expires_in": t_delta.total_seconds(), "access_token": "test_token"}
        )

    with MonkeyPatch.context() as m:
        m.setenv("CLIENT_SECRET", "test secret")
        m.setattr(requests, "post", mock_post)
        settings = TokenSettings()
        settings._fetch_keycloak_token()


@pytest.mark.filterwarnings("ignore: No secret or token given")
def test_fetch_keycloak_errors(monkeypatch):
    fail_msg = "Oh no"

    def mock_post(*args, **kwargs):
        return MockResponse(
            {"expires_in": time.time(), "access_token": "test_token"},
            raise_msg=fail_msg,
        )

    monkeypatch.delenv("CLIENT_SECRET", raising=False)
    monkeypatch.setattr(requests, "post", mock_post)
    settings = TokenSettings()
    with pytest.raises(AuthError, match="No client secret given"):
        settings._fetch_keycloak_token()

    # Set a client secret
    monkeypatch.setenv("CLIENT_SECRET", "test secret")
    settings = TokenSettings()
    settings._fetch_keycloak_token.cache_clear()
    with pytest.raises(AuthError, match=f"Failed to get Keycloak token: {fail_msg}"):
        settings._fetch_keycloak_token()


@given(t_delta=st.timedeltas())
@example(t_delta=timedelta(seconds=-1))
def test_fetch_bearer(t_delta: timedelta):
    def mock_post(*args, **kwargs):
        return MockResponse(
            {"expires_in": t_delta.total_seconds(), "access_token": "test_token"}
        )

    with MonkeyPatch.context() as m:
        m.setenv("CLIENT_SECRET", "test secret")
        m.setattr(requests, "post", mock_post)
        settings = TokenSettings()
        assert settings._fetch_bearer()


@pytest.mark.filterwarnings("ignore: Using SAML tokens")
def test_get_headers(monkeypatch):
    monkeypatch.setattr(TokenSettings, "_fetch_bearer", lambda _: "Bearer token")
    monkeypatch.setenv("CLIENT_SECRET", "test secret")
    settings = TokenSettings()
    headers = settings.get_headers()
    assert "Authorization" in headers
    assert "Bearer token" in headers.values()
    monkeypatch.setenv("SAML_TOKEN", "test token")
    settings = TokenSettings()
    headers = settings.get_headers()
    assert "Session" in headers
    assert "test token" in headers.values()
