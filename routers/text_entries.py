""" ./routers/text_entries.py"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.text_entry import TextEntry
from models.guest import Guest
from schemas.text_entry import TextEntryCreate, TextEntryResponse
from services.guest_service import get_or_create_guest

router = APIRouter()


@router.post("/text_entries/", response_model=TextEntryResponse)
def create_text_entry(text_entry: TextEntryCreate, db: Session = Depends(get_db)):
    if text_entry.user_id is None and text_entry.guest_id is None:
        raise HTTPException(
            status_code=400, detail="Either user_id or guest_id must be provided"
        )

    if text_entry.guest_id:
        guest = get_or_create_guest(db, text_entry.guest_id)
        text_entry.guest_id = guest.id

    db_text_entry = TextEntry(**text_entry.dict())
    db.add(db_text_entry)
    db.commit()
    db.refresh(db_text_entry)
    return db_text_entry


@router.get("/text_entries/", response_model=List[TextEntryResponse])
def read_text_entries(
    user_id: Optional[int] = None,
    guest_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(TextEntry)
    if user_id:
        query = query.filter(TextEntry.user_id == user_id)
    elif guest_id:
        guest = get_or_create_guest(db, guest_id)
        query = query.filter(TextEntry.guest_id == guest.id)
    else:
        raise HTTPException(
            status_code=400, detail="Either user_id or guest_id must be provided"
        )

    text_entries = query.offset(skip).limit(limit).all()
    return text_entries


@router.get("/users/{user_id}/text_entries/", response_model=List[TextEntryResponse])
def read_user_text_entries(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    text_entries = (
        db.query(TextEntry)
        .filter(TextEntry.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return text_entries


@router.get("/guests/{guest_id}/text_entries/", response_model=List[TextEntryResponse])
def read_guest_text_entries(
    guest_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    guest = get_or_create_guest(db, guest_id)
    text_entries = (
        db.query(TextEntry)
        .filter(TextEntry.guest_id == guest.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return text_entries


@router.get("/text_entries/{text_id}", response_model=TextEntryResponse)
def read_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if db_text_entry is None:
        raise HTTPException(status_code=404, detail="Text entry not found")
    return db_text_entry


@router.delete("/text_entries/{text_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if not db_text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    db.delete(db_text_entry)
    db.commit()
    return {"ok": True}
