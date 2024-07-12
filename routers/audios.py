""" ./routers/audios.py"""

from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.audio import AudioCreate, AudioResponse
from services import audio_service

router = APIRouter()


@router.post("/audios/", response_model=AudioResponse)
def create_audio(audio: AudioCreate, db: Session = Depends(get_db)):
    return audio_service.create_audio(db, audio)


@router.get("/audios/{audio_id}", response_model=AudioResponse)
def get_audio(audio_id: int, db: Session = Depends(get_db)):
    return audio_service.get_audio(db, audio_id)


@router.get("/audios/", response_model=List[AudioResponse])
def get_audios(text_entry_id: int = Query(None), db: Session = Depends(get_db)):
    return audio_service.get_audios(db, text_entry_id)


@router.get("/all-audios/", response_model=List[AudioResponse])
def get_all_audios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return audio_service.get_all_audios(db, skip, limit)


@router.delete("/audios/{audio_id}")
def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    deleted_id = audio_service.delete_audio(db, audio_id)
    return JSONResponse(
        status_code=200,
        content={"message": "Audio deleted successfully", "deleted_id": deleted_id},
    )
