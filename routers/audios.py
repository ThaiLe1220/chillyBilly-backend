""" ./routers/audios.py"""

from typing import List
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response

from schemas.audio import GeneratedAudioCreate, GeneratedAudioResponse
from models import GeneratedAudio, TextEntry, VoiceClone
from database import get_db

router = APIRouter()


@router.post("/audios/", response_model=GeneratedAudioResponse)
def create_audio(audio: GeneratedAudioCreate, db: Session = Depends(get_db)):
    text_entry = db.query(TextEntry).filter(TextEntry.id == audio.text_entry_id).first()
    if not text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")

    if audio.voice_clone_id:
        # Check if the voice clone exists and belongs to the user
        voice_clone = (
            db.query(VoiceClone).filter(VoiceClone.id == audio.voice_clone_id).first()
        )
        if not voice_clone:
            raise HTTPException(status_code=404, detail="Voice not found")

        if text_entry.user_id is None:
            raise HTTPException(
                status_code=403, detail="Guests cannot use custom voices"
            )

        if voice_clone.user_id != text_entry.user_id and not voice_clone.is_default:
            raise HTTPException(
                status_code=403, detail="Cannot use another user's voice clone"
            )

    db_audio = GeneratedAudio(**audio.dict())
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


@router.get("/audios/{audio_id}", response_model=GeneratedAudioResponse)
def read_audio(audio_id: int, db: Session = Depends(get_db)):
    db_audio = db.query(GeneratedAudio).filter(GeneratedAudio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return db_audio


# @router.get("/audios/", response_model=List[GeneratedAudioResponse])
# def read_audios(
#     user_id: int = None,
#     guest_id: str = None,
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
# ):
#     if user_id is None and guest_id is None:
#         raise HTTPException(
#             status_code=400, detail="Either user_id or guest_id must be provided"
#         )

#     query = db.query(GeneratedAudio).join(TextEntry)

#     if user_id:
#         query = query.filter(TextEntry.user_id == user_id)
#     elif guest_id:
#         guest = get_or_create_guest(db, guest_id)
#         query = query.filter(TextEntry.guest_id == guest.id)

#     audios = query.offset(skip).limit(limit).all()
#     return audios


@router.delete("/audios/{audio_id}")
def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    db_audio = db.query(GeneratedAudio).filter(GeneratedAudio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    db.delete(db_audio)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Audio deleted successfully", "deleted_id": audio_id},
    )
