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
        """Checks if path is not in excluded paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for p in excluded_paths:
            if p.endswith("*"):
                if path.startswith(p[:-1]):
                    return False
            elif path == p:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Validate all requests to secure the API
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """public method
        """
        return None
