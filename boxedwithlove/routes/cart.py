from flask import Blueprint, render_template, session

from boxedwithlove.services import cart_service
from boxedwithlove.services.product_service import get_product

cart_bp = Blueprint("cart", __name__)


def _cart_id() -> str:
    cart_id = session.get("cart_id")
    if not cart_id:
        cart_id = cart_service.new_id()
        session["cart_id"] = cart_id
    return cart_id


@cart_bp.route("/cart")
def cart_view():
    cart = cart_service.get_cart(_cart_id())
    items = []
    for item in cart.items:
        product = get_product(item.product_id)
        if not product:
            continue
        items.append(
            {
                "id": item.id,
                "product": product,
                "quantity": item.quantity,
            }
        )
    summary = cart_service.summarize_cart(cart)
    return render_template("cart.html", items=items, summary=summary)
