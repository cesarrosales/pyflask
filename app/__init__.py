from flask import Flask, jsonify
from app.api.health import health_bp
from app.api.bands import bands_bp

def create_app():
    app = Flask(__name__)

    blueprints = [
        health_bp,
        bands_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        return jsonify({"error": "Internal server error"}), 500

    return app
