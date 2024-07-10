""" ./routers/profiles.py"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.profile import UserProfile
from models.user import User
from schemas.profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse

router = APIRouter()


@router.post("/users/{user_id}/profile/", response_model=UserProfileResponse)
def create_user_profile(
    user_id: int, profile: UserProfileCreate, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.profile:
        raise HTTPException(status_code=400, detail="User already has a profile")

    db_profile = UserProfile(**profile.dict(), user_id=user_id)
    db_user.profile = db_profile
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return UserProfileResponse(
        id=db_profile.id,
        user_id=db_profile.user_id,
        first_name=db_profile.first_name,
        last_name=db_profile.last_name,
        date_of_birth=db_profile.date_of_birth,
        preferred_language=db_profile.preferred_language,
    )


@router.get("/users/{user_id}/profile/", response_model=UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return UserProfileResponse(
        id=db_profile.id,
        user_id=db_profile.user_id,
        first_name=db_profile.first_name,
        last_name=db_profile.last_name,
        date_of_birth=db_profile.date_of_birth,
        preferred_language=db_profile.preferred_language,
    )


@router.put("/users/{user_id}/profile/", response_model=UserProfileResponse)
def update_user_profile(
    user_id: int, profile_update: UserProfileUpdate, db: Session = Depends(get_db)
):
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    update_data = profile_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)

    return UserProfileResponse(
        id=db_profile.id,
        user_id=db_profile.user_id,
        first_name=db_profile.first_name,
        last_name=db_profile.last_name,
        date_of_birth=db_profile.date_of_birth,
        preferred_language=db_profile.preferred_language,
    )
