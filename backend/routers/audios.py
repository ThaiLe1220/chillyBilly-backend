""" ./backend/routers/audios.py"""

from typing import List
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.audio import AudioCreate, AudioResponse
from services import audio_service

router = APIRouter()


@router.post("/audios/", response_model=AudioResponse)
async def create_audio(
    audio: AudioCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    return await audio_service.create_audio(db, audio, background_tasks)


@router.get("/audios/{audio_id}", response_model=AudioResponse)
async def get_audio(audio_id: int, db: Session = Depends(get_db)):
    return await audio_service.get_audio(db, audio_id)


@router.get("/audios/", response_model=List[AudioResponse])
async def get_audios(
    user_id: int = Query(None),
    guest_id: int = Query(None),
    db: Session = Depends(get_db),
):
    return await audio_service.get_audios(db, user_id, guest_id)


@router.get("/all-audios/", response_model=List[AudioResponse])
async def get_all_audios(db: Session = Depends(get_db)):
    return await audio_service.get_all_audios(db)


@router.delete("/audios/{audio_id}")
async def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    deleted_id = await audio_service.delete_audio(db, audio_id)
    return JSONResponse(
        status_code=200,
        content={"message": "Audio deleted successfully", "deleted_id": deleted_id},
    )
