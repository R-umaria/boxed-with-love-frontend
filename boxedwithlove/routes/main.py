from flask import Blueprint, render_template, request

from boxedwithlove.services.product_service import list_products

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    featured = list_products()[:3]
    categories = [
        {"name": "Cozy", "description": "Warmth and comfort"},
        {"name": "Celebration", "description": "Joyful moments"},
        {"name": "Wellness", "description": "Care and calm"},
    ]
    return render_template("home.html", featured=featured, categories=categories)
