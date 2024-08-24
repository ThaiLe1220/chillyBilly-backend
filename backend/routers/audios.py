from typing import List, Optional
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.audio import AudioCreate, AudioResponse, AudioStatus
from services import audio_service

router = APIRouter()


@router.post("/audios/", response_model=AudioResponse)
async def create_audio(
    audio: AudioCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    return await audio_service.create_audio(db, audio, background_tasks)


@router.get("/audios/{audio_id}", response_model=AudioResponse)
async def get_audio(audio_id: int, db: Session = Depends(get_db)):
    audio = await audio_service.get_audio(db, audio_id)
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return audio


@router.get("/audios/", response_model=List[AudioResponse])
async def get_audios(
    user_id: Optional[int] = Query(None),
    guest_id: Optional[int] = Query(None),
    status: Optional[AudioStatus] = Query(None),
    db: Session = Depends(get_db),
):
    return await audio_service.get_audios(db, user_id, guest_id, status)


@router.get("/all-audios/", response_model=List[AudioResponse])
async def get_all_audios(
    user_id: Optional[int] = Query(None),
    guest_id: Optional[int] = Query(None),
    status: Optional[AudioStatus] = Query(None),
    db: Session = Depends(get_db),
):
    return await audio_service.get_all_audios(db, user_id, guest_id, status)


@router.delete("/audios/{audio_id}")
async def delete_audio(audio_id: int, db: Session = Depends(get_db)):
    try:
        deleted_id = await audio_service.delete_audio(db, audio_id)
        return JSONResponse(
            status_code=200,
            content={"message": "Audio deleted successfully", "deleted_id": deleted_id},
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})


@router.patch("/audios/{audio_id}/status", response_model=AudioResponse)
async def update_audio_status(
    audio_id: int, status: AudioStatus, db: Session = Depends(get_db)
):
    updated_audio = await audio_service.update_audio_status(db, audio_id, status)
    if updated_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return updated_audio
