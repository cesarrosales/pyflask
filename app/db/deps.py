from contextlib import contextmanager
from app.db.session import SessionLocal

@contextmanager
def get_db():
    # contextmanager to ensure the DB session is always closed
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()