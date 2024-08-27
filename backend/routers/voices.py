""" ./backend/routers/voices.py"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    BackgroundTasks,
    UploadFile,
    File,
    Form,
)

from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Voice, User
from schemas.voice import VoiceCreate, VoiceResponse, VoiceUpdate
from services import voice_service

router = APIRouter()


@router.post("/users/{user_id}/voices/", response_model=VoiceResponse)
async def create_voice_route(
    user_id: int,
    file: UploadFile = File(...),
    voice_name: str = Form(...),
    language: str = Form(...),
    description: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
):
    return await voice_service.create_voice(
        db, user_id, voice_name, language, description, file, background_tasks
    )


@router.get("/users/{user_id}/voices/", response_model=List[VoiceResponse])
def read_user_voices(
    user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return voice_service.get_user_voices(db, user_id, skip, limit)


@router.get("/voices/{voice_id}", response_model=VoiceResponse)
def read_voice(voice_id: int, db: Session = Depends(get_db)):
    return voice_service.get_voice(db, voice_id)


@router.delete(
    "/users/{user_id}/voices/{voice_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_voice(user_id: int, voice_id: int, db: Session = Depends(get_db)):
    await voice_service.delete_voice(db, user_id, voice_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/voices/create_defaults/", response_model=List[VoiceResponse])
def create_default_voices(db: Session = Depends(get_db)):
    base_path = "default"
    default_voices = voice_service.create_default_voices(db, base_path)
    return default_voices
