from flask import Blueprint, jsonify
from app.db.deps import get_db
from app.models.band import Band

bands_bp = Blueprint("bands", __name__, url_prefix="/bands")

@bands_bp.get("/")
def list_bands():
    with get_db() as db:
        bands = db.query(Band).order_by(Band.name).all()
        return jsonify([{"id": b.id, "name": b.name} for b in bands])