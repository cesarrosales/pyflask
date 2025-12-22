import logging
import os
from flask import Flask, jsonify, request
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
        try:
            from sqlalchemy import text
            from app.db.session import engine
        except Exception:  # pragma: no cover - best-effort diagnostics
            engine = None
        if engine is None:
            logger.warning("Database engine is not initialized; skipping identity diagnostics.")
        else:
            try:
                with engine.connect() as conn:
                    row = conn.execute(
                        text(
                            "select current_user, current_database(), "
                            "current_schema, current_setting('search_path')"
                        )
                    ).one()
                logger.info(
                    "DB identity: user=%s db=%s schema=%s search_path=%s",
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                )
            except Exception as err:  # pragma: no cover - best-effort diagnostics
                logger.error("DB identity check failed: %r", err)

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

    @app.after_request
    def log_response_details(response):
        try:
            body_len = len(response.get_data() or b"")
        except Exception:
            body_len = None
        logger.info(
            "Response: path=%s status=%s content_length=%s body_len=%s",
            getattr(request, "path", None),
            response.status_code,
            response.content_length,
            body_len,
        )
        return response

    return app
