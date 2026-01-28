from __future__ import annotations

from typing import Optional

from .data_store import USERS, User, new_id


class AuthError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.status = status


def create_user(email: str, name: str) -> User:
    if not email or not name:
        raise AuthError("INVALID_INPUT", "Email and name are required.")
    if any(user.email == email for user in USERS.values()):
        raise AuthError("EMAIL_IN_USE", "Email already registered.", status=409)
    user = User(id=new_id(), email=email, name=name)
    USERS[user.id] = user
    return user


def authenticate(email: str) -> Optional[User]:
    return next((user for user in USERS.values() if user.email == email), None)
