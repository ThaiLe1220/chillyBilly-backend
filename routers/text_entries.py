from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.text_entry import TextEntry
from schemas.text_entry import TextEntryCreate, TextEntryResponse

router = APIRouter()


@router.post("/users/{user_id}/text_entries/", response_model=TextEntryResponse)
def create_text_entry(
    user_id: int, text_entry: TextEntryCreate, db: Session = Depends(get_db)
):
    db_text_entry = TextEntry(**text_entry.dict(), user_id=user_id)
    db.add(db_text_entry)
    db.commit()
    db.refresh(db_text_entry)
    return db_text_entry


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


@router.get("/text_entries/{text_id}", response_model=TextEntryResponse)
def read_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if db_text_entry is None:
        raise HTTPException(status_code=404, detail="Text entry not found")
    return db_text_entry


@router.delete(
    "/users/{user_id}/text_entries/{text_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_text_entry(user_id: int, text_id: int, db: Session = Depends(get_db)):
    db_text_entry = (
        db.query(TextEntry)
        .filter(TextEntry.id == text_id, TextEntry.user_id == user_id)
        .first()
    )
    if not db_text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    db.delete(db_text_entry)
    db.commit()
    return {"ok": True}
