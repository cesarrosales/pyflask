from flask import Flask
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

    return app