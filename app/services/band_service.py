import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.band_repo import BandRepository

class BandService:
    def __init__(self, repo: Optional[BandRepository] = None):
        self.repo = repo or BandRepository()
        self.logger = logging.getLogger(__name__)

    def list_bands(self, db: Session):
        self.logger.info("Canary: BandService.list_bands start")
        bands = self.repo.list_bands(db)
        self.logger.info("Canary: BandService.list_bands result_count=%s", len(bands))
        return [{"id": b.id, "name": b.name} for b in bands]
