""" ./backend/services/voice_service.py"""

import os
import shutil
import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from models import Voice, User
from schemas.voice import VoiceCreate, VoiceResponse, VoiceUpdate
import random
import time


def create_voice(
    db: Session, user_id: int, voice: VoiceCreate, background_tasks: BackgroundTasks
) -> VoiceResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_voice = Voice(
        user_id=user_id,
        voice_name=voice.voice_name,
        original_file_path=voice.original_file_path,
        status="processing",
        is_default=False,
        language=voice.language,
        description=voice.description,
    )
    db.add(db_voice)
    db.commit()
    db.refresh(db_voice)

    # Start voice processing in the background
    background_tasks.add_task(asyncio.run, process_voice(db, db_voice.id))

    return VoiceResponse(
        id=db_voice.id,
        user_id=db_voice.user_id,
        voice_name=db_voice.voice_name,
        original_file_path=db_voice.original_file_path,
        processed_file_path=db_voice.processed_file_path,
        status=db_voice.status,
        is_default=db_voice.is_default,
        language=db_voice.language,
        description=db_voice.description,
        created_at=db_voice.created_at,
        updated_at=db_voice.updated_at,
    )


async def process_voice(db: Session, voice_id: int):
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if not voice:
        print(f"Voice with id {voice_id} not found")
        return

    try:
        # Wait for 10 seconds
        await asyncio.sleep(10)

        # Update voice status
        voice.status = "ready"
        voice.processed_file_path = f"/path/to/processed_voices/{voice.id}"
        db.commit()
        print(f"Voice processing completed for voice id {voice_id}")

    except Exception as e:
        # If any error occurs during processing, update status to failed
        voice.status = "failed"
        db.commit()
        print(f"Voice processing failed for voice id {voice_id}: {str(e)}")


def get_voices(db: Session, skip: int = 0, limit: int = 10) -> list[VoiceResponse]:
    voices = db.query(Voice).offset(skip).limit(limit).all()
    return [
        VoiceResponse(
            id=voice.id,
            user_id=voice.user_id,
            voice_name=voice.voice_name,
            original_file_path=voice.original_file_path,
            processed_file_path=voice.processed_file_path,
            status=voice.status,
            is_default=voice.is_default,
            language=voice.language,
            description=voice.description,
            created_at=voice.created_at,
            updated_at=voice.updated_at,
        )
        for voice in voices
    ]


def get_user_voices(
    db: Session, user_id: int, skip: int = 0, limit: int = 10
) -> list[VoiceResponse]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    voices = (
        db.query(Voice)
        .filter((Voice.user_id == user_id) | (Voice.is_default == True))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        VoiceResponse(
            id=voice.id,
            user_id=voice.user_id,
            voice_name=voice.voice_name,
            original_file_path=voice.original_file_path,
            processed_file_path=voice.processed_file_path,
            status=voice.status,
            is_default=voice.is_default,
            language=voice.language,
            description=voice.description,
            created_at=voice.created_at,
            updated_at=voice.updated_at,
        )
        for voice in voices
    ]


def get_voice(db: Session, voice_id: int) -> VoiceResponse:
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")
    return VoiceResponse(
        id=voice.id,
        user_id=voice.user_id,
        voice_name=voice.voice_name,
        original_file_path=voice.original_file_path,
        processed_file_path=voice.processed_file_path,
        status=voice.status,
        is_default=voice.is_default,
        language=voice.language,
        description=voice.description,
        created_at=voice.created_at,
        updated_at=voice.updated_at,
    )


def delete_voice(db: Session, user_id: int, voice_id: int) -> dict:
    voice = (
        db.query(Voice)
        .filter(
            Voice.id == voice_id, Voice.user_id == user_id, Voice.is_default == False
        )
        .first()
    )
    if not voice:
        raise HTTPException(
            status_code=404, detail="Voice not found or cannot be deleted"
        )
    db.delete(voice)
    db.commit()
    return {"message": f"Voice with id {voice_id} has been successfully deleted"}


def create_default_voices(db: Session, base_path: str) -> list[VoiceResponse]:
    default_voices = [
        {"voice_name": "Default English Male", "language": "en", "gender": "male"},
        {"voice_name": "Default English Female", "language": "en", "gender": "female"},
        {"voice_name": "Default Vietnamese Male", "language": "vi", "gender": "male"},
        {
            "voice_name": "Default Vietnamese Female",
            "language": "vi",
            "gender": "female",
        },
    ]

    created_voices = []

    for voice in default_voices:
        file_path = os.path.join(
            base_path, f"{voice['language']}_{voice['gender']}.mp3"
        )

        existing_voice = (
            db.query(Voice)
            .filter(Voice.voice_name == voice["voice_name"], Voice.is_default == True)
            .first()
        )

        if not existing_voice:
            db_voice = Voice(
                voice_name=voice["voice_name"],
                original_file_path=file_path,
                processed_file_path=file_path,
                status="ready",
                is_default=True,
                language=voice["language"],
                description=f"Default {voice['language'].upper()} {voice['gender'].capitalize()} voice",
            )
            db.add(db_voice)
            created_voices.append(db_voice)
        else:
            created_voices.append(existing_voice)

    db.commit()
    return [
        VoiceResponse(
            id=voice.id,
            user_id=voice.user_id,
            voice_name=voice.voice_name,
            original_file_path=voice.original_file_path,
            processed_file_path=voice.processed_file_path,
            status=voice.status,
            is_default=voice.is_default,
            language=voice.language,
            description=voice.description,
            created_at=voice.created_at,
            updated_at=voice.updated_at,
        )
        for voice in created_voices
    ]


def update_voice(
    db: Session,
    user_id: int,
    voice_id: int,
    voice_update: VoiceUpdate,
    background_tasks: BackgroundTasks,
) -> VoiceResponse:
    voice = (
        db.query(Voice)
        .filter(
            Voice.id == voice_id, Voice.user_id == user_id, Voice.is_default == False
        )
        .first()
    )
    if not voice:
        raise HTTPException(
            status_code=404,
            detail="Custom voice not found or you don't have permission to update it",
        )

    update_data = voice_update.dict(exclude_unset=True)

    # Prevent updating certain fields
    for field in ["id", "user_id", "is_default", "processed_file_path", "status"]:
        update_data.pop(field, None)

    # If original_file_path is updated, reset the processing status
    if "original_file_path" in update_data:
        update_data["status"] = "processing"
        update_data["processed_file_path"] = None

        # Start voice processing in the background
        background_tasks.add_task(asyncio.run, process_voice(db, voice.id))

    for key, value in update_data.items():
        setattr(voice, key, value)

    db.commit()
    db.refresh(voice)

    return VoiceResponse(
        id=voice.id,
        user_id=voice.user_id,
        voice_name=voice.voice_name,
        original_file_path=voice.original_file_path,
        processed_file_path=voice.processed_file_path,
        status=voice.status,
        is_default=voice.is_default,
        language=voice.language,
        description=voice.description,
        created_at=voice.created_at,
        updated_at=voice.updated_at,
    )
