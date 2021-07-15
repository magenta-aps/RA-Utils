#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import time
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from warnings import warn


try:
    import requests
    from pydantic import AnyHttpUrl
    from pydantic import BaseSettings
    from pydantic import Field
    from pydantic import root_validator
except ImportError as err:  # pragma: no cover
    raise ImportError(f"{err.name} not found - token settings not imported")


# --------------------------------------------------------------------------------------
# Exception
# --------------------------------------------------------------------------------------
class AuthError(Exception):
    """Raised when errors in authentication occurs."""


# --------------------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------------------


class TokenSettings(BaseSettings):
    client_id: str = "mo"
    client_secret: Optional[str]  # in the future, this should be required
    auth_realm: str = "mo"
    auth_server: AnyHttpUrl = Field("http://localhost:8081/auth")
    saml_token: Optional[str]  # deprecate when fully on keycloak?

    class Config:
        frozen = True

    @root_validator
    def validate_settings(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate token settings by checking that either client_secret,
        SAML token, or both exist.
        This validation occurs when TokenSettings are initialised and does
        not mutate values.

        Args:
            values (Dict[str, Any]): Initialised TokenSettings values.

        Emits:
            UserWarning: If none of CLIENT_SECRET or SAML_TOKEN are given
                during initialisation.
            PendingDeprecationWarning: If SAML_TOKEN is used.


        Returns:
            Dict[str, Any]: TokenSettings values, unchanged.
        """

        keycloak, saml = values.get("client_secret"), values.get("saml_token")
        if not any([keycloak, saml]):
            warn("No secret or token given", stacklevel=2)
        if saml:
            warn(
                "Using SAML tokens will be deprecated",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        return values

    @lru_cache(maxsize=None)
    def _fetch_keycloak_token(self) -> Tuple[float, str]:
        """Fetch a keycloak token and its expiry time.

        Raises:
            AuthError: If no client secret is given or the response from
                the authentication server raises an error.

        Returns:
            Tuple[float, str]: Token expiry and token.
        """
        token_url = (
            f"{self.auth_server}/realms/{self.auth_realm}/protocol/openid-connect/token"
        )
        if self.client_secret is None:
            raise AuthError("No client secret given")
        payload: Dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
        except requests.RequestException as err:
            raise AuthError(f"Failed to get Keycloak token: {err}")
        response_payload: Dict[str, Any] = response.json()
        expires: int = response_payload["expires_in"]
        token: str = response_payload["access_token"]
        return time.monotonic() + float(expires), token

    def _fetch_bearer(self) -> str:
        """Fetch a Keycloak bearer token.

        Returns:
            str: Bearer token.
        """
        expires, token = self._fetch_keycloak_token()
        if expires < time.monotonic():
            self._fetch_keycloak_token.cache_clear()
            _, token = self._fetch_keycloak_token()
        return "Bearer " + token

    def get_headers(self) -> Dict[str, str]:
        """Get authorization headers based on configured tokens.
        If a client secret and a SAML token are both configured,
        they will both exist in the header with keys "Authorization"
        and "Session", respectively.

        Returns:
            Dict[str, str]: Header dictionary.
        """
        headers: Dict[str, str] = {}
        if self.saml_token:
            headers["Session"] = self.saml_token
        if self.client_secret:
            headers["Authorization"] = self._fetch_bearer()
        return headers


if __name__ == "__main__":
    pass
