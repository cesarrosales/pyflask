import logging
import os
from flask import Flask, jsonify
from app.api.health import health_bp
from app.api.bands import bands_bp

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    if not os.getenv("DATABASE_URL"):
        logger.warning("DATABASE_URL is not configured; database connections are disabled.")
    else:
        logger.info("DATABASE_URL is configured.")

    blueprints = [
        health_bp,
        bands_bp,
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        try:
            from sqlalchemy.exc import OperationalError
        except ImportError:
            OperationalError = None
        if OperationalError is not None and isinstance(err, OperationalError):
            orig = getattr(err, "orig", None)
            logger.error(
                "Database connection failed: orig=%r args=%r",
                orig,
                getattr(orig, "args", None),
            )
        logger.exception("Unhandled exception", exc_info=err)
        return jsonify({"error": "Internal server error"}), 500

    return app
