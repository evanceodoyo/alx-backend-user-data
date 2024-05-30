#!/usr/bin/env python3
"""Password encryption module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Salts and hashes a password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
