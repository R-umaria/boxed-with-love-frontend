from .auth import auth_bp
from .cart import cart_bp
from .checkout import checkout_bp
from .main import main_bp
from .orders import orders_bp
from .products import products_bp

__all__ = [
    "auth_bp",
    "cart_bp",
    "checkout_bp",
    "main_bp",
    "orders_bp",
    "products_bp",
]
