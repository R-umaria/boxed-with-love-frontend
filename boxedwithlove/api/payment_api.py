from flask import jsonify, request

from . import api_bp
from .utils import error_response, require_auth
from boxedwithlove.services import payment_service


@api_bp.route("/payment-methods", methods=["GET"])
def payment_methods_list():
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    methods = payment_service.list_methods(user.id)
    data = [
        {"id": m.id, "brand": m.brand, "last4": m.last4, "expiry": m.expiry}
        for m in methods
    ]
    return jsonify({"data": data}), 200


@api_bp.route("/payment-methods", methods=["POST"])
def payment_methods_add():
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    data = request.get_json(silent=True) or {}
    try:
        method = payment_service.add_method(
            user.id, data.get("brand", ""), data.get("last4", ""), data.get("expiry", "")
        )
    except payment_service.PaymentError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return (
        jsonify(
            {
                "data": {
                    "id": method.id,
                    "brand": method.brand,
                    "last4": method.last4,
                    "expiry": method.expiry,
                }
            }
        ),
        201,
    )


@api_bp.route("/payment-methods/<method_id>", methods=["DELETE"])
def payment_methods_remove(method_id: str):
    try:
        user = require_auth()
    except PermissionError:
        payload, status = error_response("UNAUTHORIZED", "Login required.", 401)
        return jsonify(payload), status
    try:
        payment_service.remove_method(user.id, method_id)
    except payment_service.PaymentError as exc:
        payload, status = error_response(exc.code, str(exc), exc.status)
        return jsonify(payload), status
    return "", 204
