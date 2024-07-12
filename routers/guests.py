""" ./routers/guests.py"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.guest import GuestResponse
from services import guest_service

router = APIRouter()


@router.post("/guests", response_model=GuestResponse)
def create_guest(db: Session = Depends(get_db)):
    return guest_service.create_guest(db)


@router.get("/guests/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: int, db: Session = Depends(get_db)):
    guest = guest_service.get_guest(db, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


@router.get("/guests", response_model=list[GuestResponse])
def get_all_guests(db: Session = Depends(get_db)):
    return guest_service.get_all_guests(db)


@router.put("/guests/{guest_id}", response_model=GuestResponse)
def update_guest_activity(guest_id: int, db: Session = Depends(get_db)):
    guest = guest_service.update_guest_activity(db, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest


@router.delete("/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(guest_id: int, db: Session = Depends(get_db)):
    success = guest_service.delete_guest(db, guest_id)
    if not success:
        raise HTTPException(status_code=404, detail="Guest not found")


@router.delete("/guests/cleanup/")
def cleanup_guests(db: Session = Depends(get_db)):
    deleted_count = guest_service.cleanup_inactive_guests(db)
    if deleted_count > 0:
        return {"message": f"Deleted {deleted_count} inactive guests"}
    else:
        return {"message": "No inactive guests found to delete"}
