from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

from flask import redirect, request, session, url_for

from boxedwithlove.services.data_store import USERS, User


F = TypeVar("F", bound=Callable[..., object])


def get_current_user() -> User | None:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return USERS.get(user_id)


def login_required(view: F) -> F:
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
