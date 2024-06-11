#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
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
