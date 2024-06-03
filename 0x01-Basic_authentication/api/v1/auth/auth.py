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
        """public method
        """
        return False

    def authorization_header(self, request=None) -> str:
        """public method
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method
        """
        return None
