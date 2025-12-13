from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Sweet
from app.schemas import SweetOut

router = APIRouter(prefix="/api/sweets", tags=["sweets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[SweetOut])
def list_sweets(db: Session = Depends(get_db)):
    return db.query(Sweet).all()
