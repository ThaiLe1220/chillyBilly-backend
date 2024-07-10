""" ./services/guest_service.py"""

from sqlalchemy.orm import Session
from models.guest import Guest
from uuid import uuid4
from datetime import datetime


def get_or_create_guest(db: Session, guest_id: str = None):
    if guest_id:
        guest = db.query(Guest).filter(Guest.guest_id == guest_id).first()
        if guest and not guest.is_expired:
            guest.update_activity()
            db.commit()
            return guest

    # Create new guest if not found or expired
    new_guest_id = guest_id or str(uuid4())
    guest = Guest(
        guest_id=new_guest_id,
        created_at=datetime.utcnow(),  # Explicitly set created_at
        last_active_date=datetime.utcnow(),  # Explicitly set last_active_date
    )
    guest.update_activity()  # This will set the expiration_date
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


def cleanup_inactive_guests(db: Session):
    expired_guests = (
        db.query(Guest).filter(Guest.expiration_date < datetime.utcnow()).all()
    )
    for guest in expired_guests:
        db.delete(guest)
    db.commit()
