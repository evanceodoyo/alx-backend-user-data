#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    Parameters:
      password (str): user password.
    Returns:
      bytes
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


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
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
