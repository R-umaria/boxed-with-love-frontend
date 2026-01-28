from flask import jsonify, request, session

from . import api_bp
from .utils import error_response, require_auth
from boxedwithlove.services import cart_service, order_service
from boxedwithlove.services.product_service import get_product


def _cart_id() -> str:
    cart_id = session.get("cart_id")
    if not cart_id:
        cart_id = cart_service.new_id()
        session["cart_id"] = cart_id
    return cart_id


@api_bp.route("/orders", methods=["GET"])
def orders_list():
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    orders = order_service.list_orders(user.id)
    data = [
        {
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
        }
        for o in orders
    ]
    return jsonify({"data": data}), 200


@api_bp.route("/orders", methods=["POST"])
def orders_create():
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    data = request.get_json(silent=True) or {}
    shipping = data.get("shipping", {})
    cart = cart_service.get_cart(_cart_id())
    try:
        order = order_service.place_order(user.id, cart, shipping)
    except order_service.OrderError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return (
        jsonify(
            {
                "data": {
                    "id": order.id,
                    "total": order.total,
                    "status": order.status,
                    "created_at": order.created_at.isoformat(),
                }
            }
        ),
        201,
    )


@api_bp.route("/orders/<order_id>", methods=["GET"])
def orders_detail(order_id: str):
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    order = order_service.get_order(user.id, order_id)
    if not order:
        payload, status = error_response("NOT_FOUND", "Order not found.", 404)
        return jsonify(payload), status
    items = []
    for item in order.items:
        product = get_product(item.product_id)
        if not product:
            continue
        items.append(
            {
                "product_id": item.product_id,
                "name": product.name,
                "quantity": item.quantity,
                "price": product.price,
            }
        )
    return (
        jsonify(
            {
                "data": {
                    "id": order.id,
                    "total": order.total,
                    "status": order.status,
                    "created_at": order.created_at.isoformat(),
                    "items": items,
                    "shipping": order.shipping,
                }
            }
        ),
        200,
    )
