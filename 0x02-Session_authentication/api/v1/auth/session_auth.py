#!/usr/bin/env python3
"""Module for session authentication.
"""
from uuid import uuid4
from api.v1.auth.basic_auth import Auth


class SessionAuth(Auth):
    """Class for Session Authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a `user_id`
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user id based on session id
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
