""" ./routers/guests.py"""

from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from services.guest_service import get_or_create_guest, cleanup_inactive_guests
from schemas.guest import GuestResponse
from models.guest import Guest
from database import get_db

router = APIRouter()


@router.get("/guests/session", response_model=GuestResponse)
def get_or_create_guest_session(response: Response, db: Session = Depends(get_db)):
    guest = get_or_create_guest(db)
    return GuestResponse(
        id=guest.id,
        created_at=guest.created_at,
        last_active_date=guest.last_active_date,
    )


@router.get("/guests", response_model=List[GuestResponse])
def get_all_guests(db: Session = Depends(get_db)):
    guests = db.query(Guest).all()
    return [
        GuestResponse(
            id=guest.id,
            created_at=guest.created_at,
            last_active_date=guest.last_active_date,
        )
        for guest in guests
    ]


@router.get("/guests/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    if guest.is_expired:
        raise HTTPException(status_code=410, detail="Guest has expired")
    guest.update_activity()
    db.commit()
    return GuestResponse(
        id=guest.id,
        created_at=guest.created_at,
        last_active_date=guest.last_active_date,
    )


@router.put("/guests/{guest_id}/active", response_model=GuestResponse)
def update_guest_activity(guest_id: int, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    guest.update_activity()
    db.commit()
    db.refresh(guest)
    return GuestResponse(
        id=guest.id,
        created_at=guest.created_at,
        last_active_date=guest.last_active_date,
    )


@router.delete("/guests/cleanup")
def cleanup_guests(db: Session = Depends(get_db)):
    deleted_count = cleanup_inactive_guests(db)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Inactive guests cleaned up successfully",
            "deleted_count": deleted_count,
        },
    )
