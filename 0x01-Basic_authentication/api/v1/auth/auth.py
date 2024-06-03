#!/usr/bin/env python3
"""Module for authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication class.
    """
    def require_auth(
        self,
        path: str,
        excluded_paths: List[str]
    ) -> bool:
        """Checks if path is not in excluded paths and returns bool
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        return not (path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """public method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method
        """
        return None
