#!/usr/bin/env python3
"""Module for Session db authentication with expiry.
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Class for Session Database Authentication.
    """
    def create_session(self, user_id: str = None) -> str:
        """Returns session ID for a user session.
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(**{"user_id": user_id,
                                      "session_id": session_id})
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns User ID by requesting `UserSession` in
        the db based on `session_id`
        """
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if len(user_sessions) == 0:
            return None
        duration = timedelta(seconds=self.session_duration)
        exp_time = user_sessions[0].created_at + duration
        if exp_time < datetime.now():
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """Deletes user session (logout)
        """
        session_id = self.session_cookie(request)
        try:
            user_sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(user_sessions) == 0:
            return False
        user_sessions[0].remove()
        super().destroy_session(self, request)
