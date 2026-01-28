from flask import Blueprint, render_template

from boxedwithlove.routes.helpers import get_current_user, login_required
from boxedwithlove.services.order_service import get_order, list_orders
from boxedwithlove.services.product_service import get_product

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders")
@login_required
def orders_list_view():
    user = get_current_user()
    orders = list_orders(user.id) if user else []
    return render_template("orders.html", orders=orders)


@orders_bp.route("/orders/<order_id>")
@login_required
def order_detail_view(order_id: str):
    user = get_current_user()
    order = get_order(user.id, order_id) if user else None
    if not order:
        return render_template("404.html"), 404
    items = []
    for item in order.items:
        product = get_product(item.product_id)
        if not product:
            continue
        items.append({"product": product, "quantity": item.quantity})
    return render_template("order_detail.html", order=order, items=items)


@orders_bp.route("/orders/<order_id>/confirmation")
@login_required
def order_confirmation(order_id: str):
    user = get_current_user()
    order = get_order(user.id, order_id) if user else None
    if not order:
        return render_template("404.html"), 404
    return render_template("order_confirmation.html", order=order)
