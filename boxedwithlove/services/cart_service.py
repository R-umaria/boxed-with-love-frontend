from __future__ import annotations

from typing import Dict

from .data_store import CARTS, Cart, CartItem, PRODUCTS, new_id


class CartError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.status = status


def get_cart(cart_id: str) -> Cart:
    if cart_id not in CARTS:
        CARTS[cart_id] = Cart(id=cart_id)
    return CARTS[cart_id]


def add_item(cart: Cart, product_id: int, quantity: int) -> Cart:
    if quantity <= 0:
        raise CartError("INVALID_QUANTITY", "Quantity must be at least 1.")
    product = next((p for p in PRODUCTS if p.id == product_id), None)
    if not product:
        raise CartError("NOT_FOUND", "Product not found.", status=404)
    for item in cart.items:
        if item.product_id == product_id:
            item.quantity += quantity
            return cart
    cart.items.append(CartItem(id=new_id(), product_id=product_id, quantity=quantity))
    return cart


def update_item(cart: Cart, item_id: str, quantity: int) -> Cart:
    if quantity <= 0:
        raise CartError("INVALID_QUANTITY", "Quantity must be at least 1.")
    for item in cart.items:
        if item.id == item_id:
            item.quantity = quantity
            return cart
    raise CartError("NOT_FOUND", "Cart item not found.", status=404)


def remove_item(cart: Cart, item_id: str) -> Cart:
    for item in cart.items:
        if item.id == item_id:
            cart.items = [i for i in cart.items if i.id != item_id]
            return cart
    raise CartError("NOT_FOUND", "Cart item not found.", status=404)


def summarize_cart(cart: Cart) -> Dict[str, float]:
    subtotal = 0.0
    for item in cart.items:
        product = next((p for p in PRODUCTS if p.id == item.product_id), None)
        if product:
            subtotal += product.price * item.quantity
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + tax, 2)
    return {"subtotal": round(subtotal, 2), "tax": tax, "total": total}
