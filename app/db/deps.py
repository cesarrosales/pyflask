from contextlib import contextmanager
from app.db.session import SessionLocal

@contextmanager
def get_db():
    # contextmanager to ensure the DB session is always closed
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
