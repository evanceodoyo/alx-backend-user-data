#!/usr/bin/env python3
"""Module for basic authentication.
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class.
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header for
        Basic authentication.
        """
        if (
            authorization_header is None or
            not isinstance(authorization_header, str) or
            not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split()[-1]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string of the
        authorization header.
        """
        try:
            if (
                base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)
            ):
                return None

            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns user email and password from Base64 decoded value as a tuple.
        """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(":"))
