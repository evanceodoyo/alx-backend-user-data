#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
import uuid
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    Parameters:
      password (str): user password.
    Returns:
      bytes
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize session
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user.
        Parameters:
          email (str): User email
          password (str): User password
        Returns:
          User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if user is a valid user.
        Parameters:
          email (str): User email.
          password (str): User password.
        Returns:
          True is user is valid, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session.
        Parameters:
          email (str): User email.
        Returns:
          Session ID (str)
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds user based on given session id.
        Parameters:
          session_id (str): The Session ID.
        Returns:
          User if corresponding user is found, otherwise None.
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destory_session(self, user_id: int) -> None:
        """Destroys a session.
        Parameters:
          user_id (int): User id.
        Returns:
          None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token.
        Parameters:
          email (str): User email.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
