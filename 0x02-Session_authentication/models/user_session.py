#!/usr/bin/env python3
""" User module
"""
from models.base import Base


class UserSession(Base):
    """Class for User Session
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize User Session
        """
        super().__init__(*args, **kwargs)
        self.user_id: str = kwargs.get("user_id")
        self.session_id: str = kwargs.get("session_id")
