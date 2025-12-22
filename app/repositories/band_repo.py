import logging
from sqlalchemy.orm import Session
from app.models.band import Band

class BandRepository:
    def list_bands(self, db: Session) -> list[Band]:
        logger = logging.getLogger(__name__)
        logger.info("Canary: BandRepository.list_bands query start")
        bands = db.query(Band).order_by(Band.name).all()
        logger.info("Canary: BandRepository.list_bands query done result_count=%s", len(bands))
        return bands
