from fastapi import APIRouter, Depends, Query, status, HTTPException 
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Sweet
from app.schemas import SweetOut, SweetCreate

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

@router.get("/search")
def search_sweets(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Sweet)

    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)

    return query.all()

@router.post("", response_model=SweetOut, status_code=status.HTTP_201_CREATED)
def add_sweet(sweet: SweetCreate, db: Session = Depends(get_db)):
    new_sweet = Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet

@router.put("/{sweet_id}", response_model=SweetOut)
def update_sweet(sweet_id: int, sweet: SweetCreate, db: Session = Depends(get_db)):
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db_sweet.name = sweet.name
    db_sweet.category = sweet.category
    db_sweet.price = sweet.price
    db_sweet.quantity = sweet.quantity

    db.commit()
    db.refresh(db_sweet)
    return db_sweet

@router.delete("/{sweet_id}", status_code=204)
def delete_sweet(sweet_id: int, db: Session = Depends(get_db)):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(sweet)
    db.commit()
