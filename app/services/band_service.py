from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.band_repo import BandRepository

class BandService:
    def __init__(self, repo: Optional[BandRepository] = None):
        self.repo = repo or BandRepository()

    def list_bands(self, db: Session):
        bands = self.repo.list_bands(db)
        return [{"id": b.id, "name": b.name} for b in bands]