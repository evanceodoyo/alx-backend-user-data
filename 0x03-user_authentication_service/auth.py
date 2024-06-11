#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
import uuid
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
