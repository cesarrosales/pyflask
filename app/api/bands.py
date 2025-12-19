from flask import Blueprint, jsonify
from app.db.deps import get_db
from app.services.band_service import BandService
from app.security.auth import require_auth
from app.security.permissions import require_permission


bands_bp = Blueprint("bands", __name__, url_prefix="/bands")
service = BandService()

@bands_bp.get("/")
@require_auth
@require_permission("read:all")
def list_bands():
    with get_db() as db:
        output = service.list_bands(db)
        return jsonify(output)