""" ./routers/voice_clones.py"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import VoiceClone, User
from schemas.voice_clone import VoiceCloneCreate, VoiceCloneResponse

router = APIRouter()


@router.post("/users/{user_id}/voice_clones/", response_model=VoiceCloneResponse)
def create_voice_clone(
    user_id: int, voice_clone: VoiceCloneCreate, db: Session = Depends(get_db)
):
    db_voice_clone = VoiceClone(
        **voice_clone.dict(), user_id=user_id, status="processing", is_default=False
    )
    db.add(db_voice_clone)
    db.commit()
    db.refresh(db_voice_clone)
    return db_voice_clone


@router.get("/users/{user_id}/voice_clones/", response_model=List[VoiceCloneResponse])
def read_user_voice_clones(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_voice_clones = (
        db.query(VoiceClone)
        .filter((VoiceClone.user_id == user_id) | (VoiceClone.is_default is True))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return user_voice_clones


@router.get("/voice_clones/{voice_id}", response_model=VoiceCloneResponse)
def read_voice_clone(voice_id: int, db: Session = Depends(get_db)):
    db_voice_clone = db.query(VoiceClone).filter(VoiceClone.id == voice_id).first()
    if db_voice_clone is None:
        raise HTTPException(status_code=404, detail="Voice clone not found")
    return db_voice_clone


@router.delete(
    "/users/{user_id}/voice_clones/{voice_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_voice_clone(user_id: int, voice_id: int, db: Session = Depends(get_db)):
    db_voice_clone = (
        db.query(VoiceClone)
        .filter(
            VoiceClone.id == voice_id,
            VoiceClone.user_id == user_id,
            VoiceClone.is_default is False,
        )
        .first()
    )
    if not db_voice_clone:
        raise HTTPException(status_code=404, detail="Voice clone not found")
    db.delete(db_voice_clone)
    db.commit()
    return {"ok": True}
