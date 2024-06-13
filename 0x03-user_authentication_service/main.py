#!/usr/bin/env python3
"""
Main file
"""
import requests


BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test POST /users
    Parameters:
      email (str): User email.
      password (str): User password.
    Returns:
      None
    """
    payload = {"email": email, "password": password}
    res = requests.post(BASE_URL + "/users", data=payload)
    assert res.status_code == 200
    assert res.json() == {'email': email,
                          'message': 'user created'}

    res = requests.post(BASE_URL + "/users", data=payload)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test POST /sessions with wrong password.
    Parameters:
      email (str): User email.
      password (str): User password.
    Returns:
      None
    """
    payload = {"email": email, "password": password}
    res = requests.post(BASE_URL + "/sessions", data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test POST /sessions with correct password.
    Parameters:
      email (str): User email.
      password (str): User password.
    Returns:
      User Session ID (str).
    """
    payload = {"email": email, "password": password}
    res = requests.post(BASE_URL + "/sessions", data=payload)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test GET /profile when not logged in.
    Returns:
      None
    """
    res = requests.get(BASE_URL + "/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test GET /profile when logged in.
    Parameters:
      session_id (str): User session ID.
    Returns:
      None
    """
    session_cookies = {"session_id": session_id}
    res = requests.get(BASE_URL + "/profile", cookies=session_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test DELETE /logout.
    Parameters:
      session_id (str): User session ID.
    Returns:
      None
    """
    session_cookies = {"session_id": session_id}
    res = requests.delete(BASE_URL + "/sessions", cookies=session_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test POST /reset_password.
    Parameters:
      email (str): User email.
    Returns:
      Rest password token (str).
    """
    payload = {"email": email}
    res = requests.post(BASE_URL + "/reset_password", data=payload)
    res.status_code == 200
    assert "email" in res.json()
    assert res.json().get("email") == email
    assert "reset_token" in res.json()
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test PUT /reset_password.
    Parameters:
      email (str): User email.
      reset_token (str): Reset password token.
      password (str): User password.
    Returns:
      None.
    """
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put(BASE_URL + "/reset_password", data=payload)
    res.status_code == 200
    res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
