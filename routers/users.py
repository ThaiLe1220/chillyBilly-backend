""" ./routers/users.py"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response
from services.user_service import hash_password, verify_password
from schemas.user import UserCreate, UserUpdate, UserResponse, PasswordVerification
from models.user import User
from database import get_db

router = APIRouter()


@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        two_factor_enabled=False,
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

    # return db_user
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        two_factor_enabled=db_user.two_factor_enabled,
        created_at=db_user.created_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )


@router.post("/users/{user_id}/verify_password", status_code=status.HTTP_200_OK)
def verify_user_password(
    user_id: int,
    password_verification: PasswordVerification,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if verify_password(password_verification.password, db_user.password_hash):
        return {"message": "Password is correct"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect password")


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.dict(exclude_unset=True)

    if "username" in update_data:
        existing_user = (
            db.query(User).filter(User.username == update_data["username"]).first()
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Username already exists")
        db_user.username = update_data["username"]

    if "email" in update_data:
        db_user.email = update_data["email"]

    if "password" in update_data:
        db_user.password_hash = hash_password(update_data["password"])

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="An integrity error occurred"
        ) from e

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        two_factor_enabled=db_user.two_factor_enabled,
        created_at=db_user.created_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(db_user)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User deleted successfully", "deleted_id": user_id},
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Unable to delete user due to existing references"
        ) from e


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = db.query(User).offset(skip).limit(limit).all()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            two_factor_enabled=user.two_factor_enabled,
            created_at=user.created_at,
            last_login=user.last_login,
            last_active_date=user.last_active_date,
        )
        for user in db_users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        two_factor_enabled=db_user.two_factor_enabled,
        created_at=db_user.created_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )
