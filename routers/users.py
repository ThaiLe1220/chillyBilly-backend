from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from utils import hash_password

router = APIRouter()


@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="Username already exists"
            ) from e
        elif "email" in str(e.orig):
            raise HTTPException(
                status_code=400, detail="Email already registered"
            ) from e
        else:
            raise HTTPException(
                status_code=400, detail="An integrity error occurred"
            ) from e
    return db_user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)

    if "email" in update_data:
        db_user.email = update_data["email"]

    if "password" in update_data:
        db_user.password_hash = hash_password(update_data["password"])

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(db_user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Unable to delete user due to existing references"
        ) from e

    return {"ok": True}


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
