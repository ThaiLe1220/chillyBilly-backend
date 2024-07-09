""" ./routers/guests.py"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from models.guest import Guest
from schemas.guest import GuestCreate, GuestResponse
from schemas.user import UserCreate, UserResponse
from datetime import datetime, timedelta
from uuid import uuid4
from services.guest_service import get_or_create_guest, cleanup_inactive_guests

# from services.user_service import create_user, transfer_guest_data_to_user

router = APIRouter()


@router.get("/guests/session", response_model=GuestResponse)
def get_or_create_guest_session(
    response: Response, guest_id: str = None, db: Session = Depends(get_db)
):
    guest = get_or_create_guest(db, guest_id)
    response.set_cookie(
        key="guest_id", value=guest.guest_id, max_age=30 * 24 * 60 * 60
    )  # 30 days
    return guest


@router.get("/guests/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: str, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.guest_id == guest_id).first()
    if guest is None or guest.is_expired:
        raise HTTPException(status_code=404, detail="Guest not found or expired")
    guest.update_activity()
    db.commit()
    return guest


@router.put("/guests/{guest_id}/active", response_model=GuestResponse)
def update_guest_activity(guest_id: str, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.guest_id == guest_id).first()
    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.update_activity()
    db.commit()
    db.refresh(guest)
    return guest


# @router.post("/guests/{guest_id}/convert", response_model=UserResponse)
# def convert_guest_to_user(
#     guest_id: str, user_data: UserCreate, db: Session = Depends(get_db)
# ):
#     guest = db.query(Guest).filter(Guest.guest_id == guest_id).first()
#     if not guest:
#         raise HTTPException(status_code=404, detail="Guest not found")

#     new_user = create_user(db, user_data)
#     transfer_guest_data_to_user(db, guest, new_user)

#     return new_user


@router.delete("/guests/cleanup", status_code=204)
def cleanup_guests(db: Session = Depends(get_db)):
    cleanup_inactive_guests(db)
    return Response(status_code=204)
