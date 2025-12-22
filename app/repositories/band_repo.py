from sqlalchemy.orm import Session
from app.models.band import Band

class BandRepository:
    def list_bands(self, db: Session) -> list[Band]:
        return db.query(Band).order_by(Band.name).all()
