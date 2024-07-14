""" ./backend/routers/text_entries.py"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.text_entry import TextEntryCreate, TextEntryResponse
from services import text_entry_service

router = APIRouter()


@router.post("/text_entries/", response_model=TextEntryResponse)
def create_text_entry(text_entry: TextEntryCreate, db: Session = Depends(get_db)):
    return text_entry_service.create_text_entry(db, text_entry)


@router.get("/all_text_entries/", response_model=List[TextEntryResponse])
def read_all_text_entries(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return text_entry_service.get_all_text_entries(db, skip, limit)


@router.get("/text_entries/", response_model=List[TextEntryResponse])
def read_text_entries(
    user_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return text_entry_service.get_text_entries(db, user_id, guest_id, skip, limit)


@router.get("/guests/{guest_id}/text_entries/", response_model=List[TextEntryResponse])
def read_guest_text_entries(
    guest_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return text_entry_service.get_guest_text_entries(db, guest_id, skip, limit)


@router.get("/users/{user_id}/text_entries/", response_model=List[TextEntryResponse])
def read_user_text_entries(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return text_entry_service.get_user_text_entries(db, user_id, skip, limit)


@router.get("/text_entries/{text_id}", response_model=TextEntryResponse)
def read_text_entry(text_id: int, db: Session = Depends(get_db)):
    return text_entry_service.get_text_entry(db, text_id)


@router.delete("/text_entries/{text_id}")
def delete_text_entry(text_id: int, db: Session = Depends(get_db)):
    deleted_id = text_entry_service.delete_text_entry(db, text_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Text entry deleted successfully",
            "deleted_id": deleted_id,
        },
    )
