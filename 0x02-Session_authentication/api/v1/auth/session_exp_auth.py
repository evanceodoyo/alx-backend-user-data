#!/usr/bin/env python3
"""Module for Session authentication with expiry.
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Class for Session authentication with expiry.
    """
    def __init__(self):
        """Initialize.
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create session.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        sesssion_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = sesssion_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user id from the session dictionary.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get("user_id")
