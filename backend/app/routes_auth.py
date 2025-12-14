from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.auth import create_access_token, hash_password, verify_password
import secrets
from app.dependencies import get_db, get_current_user

router = APIRouter()
import os

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


@router.post("/register", status_code=201, response_model=UserResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=(user.email == ADMIN_EMAIL)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "is_admin": new_user.is_admin
    }

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": db_user.id,
        "is_admin": db_user.is_admin
    })


    return {
        "access_token": token,
        "token_type": "bearer",
        "is_admin": db_user.is_admin
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
