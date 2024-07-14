""" ./backend/services/guest_service.py"""

from sqlalchemy.orm import Session
from models.guest import Guest
from schemas.guest import GuestResponse
from datetime import datetime, timedelta


def create_guest(db: Session) -> GuestResponse:
    guest = Guest()
    guest.update_activity()
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return GuestResponse(
        id=guest.id,
        created_at=guest.created_at,
        last_active_date=guest.last_active_date,
        expiration_date=guest.expiration_date,
    )


def get_guest(db: Session, guest_id: int) -> GuestResponse | None:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if guest:
        return GuestResponse(
            id=guest.id,
            created_at=guest.created_at,
            last_active_date=guest.last_active_date,
            expiration_date=guest.expiration_date,
        )
    return None


def get_all_guests(db: Session) -> list[GuestResponse]:
    guests = db.query(Guest).all()
    return [
        GuestResponse(
            id=guest.id,
            created_at=guest.created_at,
            last_active_date=guest.last_active_date,
            expiration_date=guest.expiration_date,
        )
        for guest in guests
    ]


def update_guest_activity(db: Session, guest_id: int) -> GuestResponse | None:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if guest:
        guest.update_activity()
        db.commit()
        db.refresh(guest)
        return GuestResponse(
            id=guest.id,
            created_at=guest.created_at,
            last_active_date=guest.last_active_date,
            expiration_date=guest.expiration_date,
        )
    return None


def delete_guest(db: Session, guest_id: int) -> bool:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if guest:
        db.delete(guest)
        db.commit()
        return True
    return False


def cleanup_inactive_guests(db: Session) -> int:
    # one_minutes_ago = datetime.utcnow() - timedelta(minutes=1)
    one_week_ago = datetime.utcnow() - timedelta(weeks=1)

    expired_guests = db.query(Guest).filter(Guest.last_active_date < one_week_ago).all()
    count = len(expired_guests)
    for guest in expired_guests:
        db.delete(guest)
    db.commit()
    return count
