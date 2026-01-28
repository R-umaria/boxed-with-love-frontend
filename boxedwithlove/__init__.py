from __future__ import annotations

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from boxedwithlove.api import api_bp
from boxedwithlove.config import Config
from boxedwithlove.routes import auth_bp, cart_bp, checkout_bp, main_bp, orders_bp, products_bp
from boxedwithlove.routes.helpers import get_current_user


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_globals():
        return {"current_user": get_current_user()}

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return "", 204

    @app.after_request
    def add_cors_headers(response):
        response.headers.setdefault("Access-Control-Allow-Origin", "*")
        response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(exc: HTTPException):
        if request.path.startswith("/api"):
            payload = {
                "error": {
                    "code": exc.name.replace(" ", "_").upper(),
                    "message": exc.description,
                    "details": {},
                }
            }
            return jsonify(payload), exc.code or 500
        return exc

    @app.errorhandler(Exception)
    def handle_generic_error(exc: Exception):
        if request.path.startswith("/api"):
            payload = {
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Something went wrong.",
                    "details": {},
                }
            }
            return jsonify(payload), 500
        raise exc

    return app
