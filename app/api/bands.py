import json
import logging

from flask import Blueprint, jsonify
from sqlalchemy import text

from app.db.session import engine
from app.utils.serialize import serialize_rows
from app.security.auth import require_auth
from app.security.permissions import require_permission


bands_bp = Blueprint("bands", __name__, url_prefix="/bands")
log = logging.getLogger(__name__)

@bands_bp.get("/")
@require_auth
@require_permission("read:all")
def list_bands():
    with engine.connect() as conn:
        rows = conn.execute(text("select * from public.bands")).fetchall()
    data = serialize_rows(rows)
    payload = json.dumps(data, default=str)
    log.info(
        "Returning JSON bytes=%d preview=%s",
        len(payload.encode("utf-8")),
        payload[:200],
    )
    return jsonify(data), 200
