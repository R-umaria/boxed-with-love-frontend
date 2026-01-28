from flask import Blueprint, render_template, session

from boxedwithlove.routes.helpers import login_required
from boxedwithlove.services import cart_service, payment_service
from boxedwithlove.services.product_service import get_product
from boxedwithlove.routes.helpers import get_current_user

checkout_bp = Blueprint("checkout", __name__)


def _cart_id() -> str:
    cart_id = session.get("cart_id")
    if not cart_id:
        cart_id = cart_service.new_id()
        session["cart_id"] = cart_id
    return cart_id


@checkout_bp.route("/checkout")
@login_required
def checkout_view():
    user = get_current_user()
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
    methods = payment_service.list_methods(user.id) if user else []
    return render_template(
        "checkout.html",
        items=items,
        summary=summary,
        methods=methods,
    )
