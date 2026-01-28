from __future__ import annotations

from typing import Any

from flask import session

from boxedwithlove.services.data_store import USERS, User


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return USERS.get(user_id)


def require_auth() -> User:
    user = get_current_user()
    if not user:
        raise PermissionError("AUTH_REQUIRED")
    return user


def error_response(code: str, message: str, status: int, details: dict[str, Any] | None = None):
    payload = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }
    return payload, status
