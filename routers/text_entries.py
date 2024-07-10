""" ./routers/text_entries.py"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from schemas.text_entry import TextEntryCreate, TextEntryResponse
from models.text_entry import TextEntry
from models.guest import Guest
from database import get_db

router = APIRouter()


@router.post("/text_entries/", response_model=TextEntryResponse)
def create_text_entry(text_entry: TextEntryCreate, db: Session = Depends(get_db)):
    if text_entry.user_id is None and text_entry.guest_id is None:
        raise HTTPException(
            status_code=400, detail="Either user_id or guest_id must be provided"
        )

    db_text_entry = TextEntry(**text_entry.dict(exclude_unset=True))
    db.add(db_text_entry)
    db.commit()
    db.refresh(db_text_entry)

    # Create a TextEntryResponse object
    response = TextEntryResponse(
        id=db_text_entry.id,
        content=db_text_entry.content,
        language=db_text_entry.language,
        created_at=db_text_entry.created_at,
    )
    return response


@router.get("/all_text_entries/", response_model=List[TextEntryResponse])
def read_all_text_entries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    text_entries = db.query(TextEntry).offset(skip).limit(limit).all()
    return [
        TextEntryResponse(
            id=entry.id,
            content=entry.content,
            language=entry.language,
            created_at=entry.created_at,
        )
        for entry in text_entries
    ]


@router.get("/text_entries/", response_model=List[TextEntryResponse])
def read_text_entries(
    user_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(TextEntry)
    if user_id:
        query = query.filter(TextEntry.user_id == user_id)
    elif guest_id:
        query = query.filter(TextEntry.guest_id == guest_id)
    else:
        raise HTTPException(
            status_code=400, detail="Either user_id or guest_id must be provided"
        )

    text_entries = query.offset(skip).limit(limit).all()
    return [
        TextEntryResponse(
            id=entry.id,
            content=entry.content,
            language=entry.language,
            created_at=entry.created_at,
        )
        for entry in text_entries
    ]


@router.get("/guests/{guest_id}/text_entries/", response_model=List[TextEntryResponse])
def read_guest_text_entries(
    guest_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    text_entries = (
        db.query(TextEntry)
        .filter(TextEntry.guest_id == guest_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        TextEntryResponse(
            id=entry.id,
            content=entry.content,
            language=entry.language,
            created_at=entry.created_at,
        )
        for entry in text_entries
    ]


@router.get("/users/{user_id}/text_entries/", response_model=List[TextEntryResponse])
def read_user_text_entries(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    text_entries = (
        db.query(TextEntry)
        .filter(TextEntry.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        TextEntryResponse(
            id=entry.id,
            content=entry.content,
            language=entry.language,
            created_at=entry.created_at,
        )
        for entry in text_entries
    ]


@router.get("/text_entries/{text_id}", response_model=TextEntryResponse)
def read_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if db_text_entry is None:
        raise HTTPException(status_code=404, detail="Text entry not found")
    return db_text_entry


@router.delete("/text_entries/{text_id}")
def delete_text_entry(text_id: int, db: Session = Depends(get_db)):
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if not db_text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    db.delete(db_text_entry)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Text entry deleted successfully", "deleted_id": text_id},
    )
