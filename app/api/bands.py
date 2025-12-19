from flask import Blueprint, jsonify
from app.db.deps import get_db
from app.services.band_service import BandService
from app.security.firebase_auth import require_firebase_token


bands_bp = Blueprint("bands", __name__, url_prefix="/bands")
service = BandService()

@bands_bp.get("/")
@require_firebase_token
def list_bands():
    with get_db() as db:
        output = service.list_bands(db)
        return jsonify(output)