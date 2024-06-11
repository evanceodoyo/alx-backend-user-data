#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password.
    Parameters:
      password (str): user password.
    Returns:
      bytes
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
