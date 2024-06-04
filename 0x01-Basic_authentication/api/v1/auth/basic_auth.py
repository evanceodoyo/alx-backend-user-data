#!/usr/bin/env python3
"""Module for basic authentication.
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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
        """Returns user email and password from Base64 decoded
        value as a tuple.
        """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ":" not in decoded_base64_authorization_header
        ):
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """Returns `User` instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
