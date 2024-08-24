""" ./backend/services/text_entry_service.py"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.text_entry import TextEntry
from models.user import User
from models.guest import Guest
from datetime import datetime
from schemas.text_entry import TextEntryCreate, TextEntryResponse


def create_text_entry(db: Session, text_entry: TextEntryCreate) -> TextEntryResponse:
    if text_entry.user_id is None and text_entry.guest_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or guest_id must be provided",
        )

    if text_entry.user_id is not None and text_entry.guest_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only one of user_id or guest_id should be provided",
        )

    # Check if user exists
    if text_entry.user_id is not None:
        user = db.query(User).filter(User.id == text_entry.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {text_entry.user_id} not found",
            )

    # Check if guest exists
    if text_entry.guest_id is not None:
        guest = db.query(Guest).filter(Guest.id == text_entry.guest_id).first()
        if not guest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Guest with id {text_entry.guest_id} not found",
            )

    # Validate language
    if text_entry.language not in ["vi", "en"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language must be either 'vi' or 'en'",
        )

    try:
        db_text_entry = TextEntry(
            content=text_entry.content,
            language=text_entry.language,
            tab_generation_id=text_entry.tab_generation_id,
            user_id=text_entry.user_id,
            created_at=datetime.utcnow()  # Use current time or provide if necessary
        )
        db.add(db_text_entry)
        db.commit()
        db.refresh(db_text_entry)

        return TextEntryResponse(
            id=db_text_entry.id,
            content=db_text_entry.content,
            language=db_text_entry.language,
            created_at=db_text_entry.created_at,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the text entry: {str(e)}",
        ) from e


def get_all_text_entries(
    db: Session, skip: int = 0, limit: int = 10
) -> List[TextEntryResponse]:
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


def get_text_entries(
    db: Session,
    user_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
) -> List[TextEntryResponse]:
    query = db.query(TextEntry)
    if user_id:
        query = query.filter(TextEntry.user_id == user_id)
    elif guest_id:
        query = query.filter(TextEntry.guest_id == guest_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or guest_id must be provided",
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


def get_guest_text_entries(
    db: Session, guest_id: int, skip: int = 0, limit: int = 10
) -> List[TextEntryResponse]:
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


def get_user_text_entries(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> List[TextEntryResponse]:
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


def get_text_entry(db: Session, text_id: int) -> TextEntryResponse:
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if db_text_entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Text entry not found"
        )
    return TextEntryResponse(
        id=db_text_entry.id,
        content=db_text_entry.content,
        language=db_text_entry.language,
        created_at=db_text_entry.created_at,
    )


def delete_text_entry(db: Session, text_id: int) -> int:
    db_text_entry = db.query(TextEntry).filter(TextEntry.id == text_id).first()
    if not db_text_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Text entry not found"
        )
    db.delete(db_text_entry)
    db.commit()
    return text_id
