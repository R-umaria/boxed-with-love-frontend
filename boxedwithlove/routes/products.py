from flask import Blueprint, render_template, request

from boxedwithlove.services.product_service import get_product, list_products

products_bp = Blueprint("products", __name__)


@products_bp.route("/products")
def product_list():
    search = request.args.get("search")
    sort = request.args.get("sort", "popular")
    products = list_products(search=search, sort=sort)
    return render_template(
        "products.html",
        products=products,
        search=search or "",
        sort=sort,
    )


@products_bp.route("/products/<int:product_id>")
def product_detail(product_id: int):
    product = get_product(product_id)
    if not product:
        return render_template("404.html"), 404
    return render_template("product_detail.html", product=product)
