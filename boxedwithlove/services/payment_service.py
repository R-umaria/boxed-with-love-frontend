from __future__ import annotations

from typing import List

from .data_store import PAYMENT_METHODS, PaymentMethod, new_id


class PaymentError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.status = status


def list_methods(user_id: str) -> List[PaymentMethod]:
    return PAYMENT_METHODS.get(user_id, [])


def add_method(user_id: str, brand: str, last4: str, expiry: str) -> PaymentMethod:
    if not (brand and last4 and expiry):
        raise PaymentError("INVALID_INPUT", "Brand, last4, and expiry are required.")
    method = PaymentMethod(id=new_id(), brand=brand, last4=last4, expiry=expiry)
    PAYMENT_METHODS.setdefault(user_id, []).append(method)
    return method


def remove_method(user_id: str, method_id: str) -> None:
    methods = PAYMENT_METHODS.get(user_id, [])
    updated = [m for m in methods if m.id != method_id]
    if len(updated) == len(methods):
        raise PaymentError("NOT_FOUND", "Payment method not found.", status=404)
    PAYMENT_METHODS[user_id] = updated
