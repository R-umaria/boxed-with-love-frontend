from flask import jsonify, request

from . import api_bp
from .utils import error_response
from boxedwithlove.services.product_service import get_product, list_products


@api_bp.route("/products", methods=["GET"])
def products_list():
    search = request.args.get("search")
    sort = request.args.get("sort", "popular")
    products = list_products(search=search, sort=sort)
    data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "rating": p.rating,
            "category": p.category,
        }
        for p in products
    ]
    return jsonify({"data": data}), 200


@api_bp.route("/products/<int:product_id>", methods=["GET"])
def product_detail(product_id: int):
    product = get_product(product_id)
    if not product:
        payload, status = error_response("NOT_FOUND", "Product not found.", 404)
        return jsonify(payload), status
    return (
        jsonify(
            {
                "data": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "rating": product.rating,
                    "category": product.category,
                    "whats_inside": product.whats_inside,
                }
            }
        ),
        200,
    )
