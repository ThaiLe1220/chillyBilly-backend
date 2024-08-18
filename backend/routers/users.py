""" ./backend/routers/users.py """

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    PasswordVerification,
    UserLogin,
    LoginResponse,
)
from services import user_service
from database import get_db

router = APIRouter()


@router.post(
    "/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.post("/users/{user_id}/verify_password", status_code=status.HTTP_200_OK)
def verify_user_password(
    user_id: int,
    password_verification: PasswordVerification,
    db: Session = Depends(get_db),
):
    user_service.verify_user_password(db, user_id, password_verification.password)
    return {"message": "Password is correct"}


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user_update)


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_id = user_service.delete_user(db, user_id)
    return {"message": "User deleted successfully", "deleted_id": deleted_id}


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print("Here")
    return user_service.get_users(db, skip, limit)


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.post("/login", response_model=LoginResponse)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(db, user_login.username, user_login.password)
