from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

from . import cart_api, orders_api, payment_api, products_api  # noqa: E402,F401
