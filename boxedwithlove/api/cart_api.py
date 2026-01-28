from flask import jsonify, request, session

from . import api_bp
from .utils import error_response
from boxedwithlove.services import cart_service
from boxedwithlove.services.product_service import get_product


def _cart_id() -> str:
    cart_id = session.get("cart_id")
    if not cart_id:
        cart_id = cart_service.new_id()
        session["cart_id"] = cart_id
    return cart_id


def _serialize_cart(cart):
    items = []
    for item in cart.items:
        product = get_product(item.product_id)
        if not product:
            continue
        items.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "line_total": round(product.price * item.quantity, 2),
            }
        )
    summary = cart_service.summarize_cart(cart)
    return {"items": items, "summary": summary}


@api_bp.route("/cart", methods=["GET"])
def cart_detail():
    cart = cart_service.get_cart(_cart_id())
    return jsonify({"data": _serialize_cart(cart)}), 200


@api_bp.route("/cart/items", methods=["POST"])
def cart_add_item():
    data = request.get_json(silent=True) or {}
    try:
        product_id = int(data.get("product_id"))
        quantity = int(data.get("quantity", 1))
    except (TypeError, ValueError):
        payload, status = error_response("INVALID_INPUT", "Invalid product or quantity.", 400)
        return jsonify(payload), status
    cart = cart_service.get_cart(_cart_id())
    try:
        cart_service.add_item(cart, product_id, quantity)
    except cart_service.CartError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return jsonify({"data": _serialize_cart(cart)}), 201


@api_bp.route("/cart/items/<item_id>", methods=["PATCH"])
def cart_update_item(item_id: str):
    data = request.get_json(silent=True) or {}
    try:
        quantity = int(data.get("quantity"))
    except (TypeError, ValueError):
        payload, status = error_response("INVALID_INPUT", "Invalid quantity.", 400)
        return jsonify(payload), status
    cart = cart_service.get_cart(_cart_id())
    try:
        cart_service.update_item(cart, item_id, quantity)
    except cart_service.CartError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return jsonify({"data": _serialize_cart(cart)}), 200


@api_bp.route("/cart/items/<item_id>", methods=["DELETE"])
def cart_remove_item(item_id: str):
    cart = cart_service.get_cart(_cart_id())
    try:
        cart_service.remove_item(cart, item_id)
    except cart_service.CartError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return "", 204
