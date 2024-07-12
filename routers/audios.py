# routers/audios.py

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.audio import AudioCreate, AudioResponse
from services import audio_service

router = APIRouter()


@router.post("/generate_audio/", response_model=AudioResponse)
def generate_audio_endpoint(
    text_entry_id: int, voice_id: int = None, db: Session = Depends(get_db)
):
    return audio_service.generate_audio(db, text_entry_id, voice_id)


@router.get("/audios/{audio_id}", response_model=AudioResponse)
def read_audio(audio_id: int, db: Session = Depends(get_db)):
    return audio_service.get_audio(db, audio_id)


@router.delete("/audios/{audio_id}")
def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    deleted_id = audio_service.delete_audio(db, audio_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Audio deleted successfully", "deleted_id": deleted_id},
    )
