""" ./services/user_service.py """

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRole
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_user(db: Session, user: UserCreate) -> UserResponse:
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        two_factor_enabled=False,
        role=UserRole(user.role),
        is_active=True,
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

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        two_factor_enabled=db_user.two_factor_enabled,
        is_active=db_user.is_active,
        role=db_user.role.value,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )


def verify_user_password(db: Session, user_id: int, password: str) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return True


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserResponse:
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

    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(db_user, key, value)

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
        is_active=db_user.is_active,
        role=db_user.role.value,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )


def delete_user(db: Session, user_id: int) -> int:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        db.delete(db_user)
        db.commit()
        return user_id
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Unable to delete user due to existing references"
        ) from e


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[UserResponse]:
    db_users = db.query(User).offset(skip).limit(limit).all()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            two_factor_enabled=user.two_factor_enabled,
            is_active=user.is_active,
            role=user.role.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            last_active_date=user.last_active_date,
        )
        for user in db_users
    ]


def get_user(db: Session, user_id: int) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        two_factor_enabled=db_user.two_factor_enabled,
        is_active=db_user.is_active,
        role=db_user.role.value,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
        last_login=db_user.last_login,
        last_active_date=db_user.last_active_date,
    )
