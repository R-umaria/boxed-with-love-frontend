from __future__ import annotations

from datetime import datetime
from typing import List

from .cart_service import summarize_cart
from .data_store import Cart, ORDERS, Order, new_id


class OrderError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.status = status


def list_orders(user_id: str) -> List[Order]:
    return ORDERS.get(user_id, [])


def get_order(user_id: str, order_id: str) -> Order | None:
    return next((o for o in ORDERS.get(user_id, []) if o.id == order_id), None)


def place_order(user_id: str, cart: Cart, shipping: dict[str, str]) -> Order:
    if not cart.items:
        raise OrderError("CART_EMPTY", "Your cart is empty.", status=400)
    summary = summarize_cart(cart)
    order = Order(
        id=new_id(),
        user_id=user_id,
        items=list(cart.items),
        total=summary["total"],
        status="Processing",
        created_at=datetime.utcnow(),
        shipping=shipping,
    )
    ORDERS.setdefault(user_id, []).append(order)
    cart.items = []
    return order
