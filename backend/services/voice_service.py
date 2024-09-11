""" ./backend/services/voice_service.py"""

import os
import aiofiles
import shutil
import aiohttp
import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks, UploadFile
from models import Voice, User
from schemas.voice import VoiceCreate, VoiceResponse, VoiceUpdate, VoiceStatus
import random
from typing import Optional


TTS_API_URL = os.getenv("TTS_API_URL", "http://localhost:8080")


import tempfile
import os

import mimetypes


async def create_voice(
    db: Session,
    user_id: int,
    voice_name: str,
    language: str,
    description: Optional[str],
    file: UploadFile,
    background_tasks: BackgroundTasks,
) -> VoiceResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(file.filename)[1]
    ) as temp_file:
        temp_file_path = temp_file.name

    # Write the file content asynchronously
    async with aiofiles.open(temp_file_path, "wb") as temp_file:
        content = await file.read()
        await temp_file.write(content)

    db_voice = Voice(
        user_id=user_id,
        voice_name=voice_name,
        original_file_path=file.filename,
        status=VoiceStatus.CREATED,
        is_default=False,
        language=language,
        description=description,
    )
    db.add(db_voice)
    db.commit()
    db.refresh(db_voice)

    # Start voice processing in the background
    background_tasks.add_task(
        process_voice, db, db_voice.id, temp_file_path, file.filename, file.content_type
    )

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
        total_length=db_voice.total_length,
        created_at=db_voice.created_at,
        updated_at=db_voice.updated_at,
    )


async def process_voice(
    db: Session,
    voice_id: int,
    temp_file_path: str,
    original_filename: str,
    content_type: str,
):
    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if not voice:
        print(f"Voice with id {voice_id} not found")
        return
    try:
        # Add voice to TTS API
        with open(temp_file_path, "rb") as file:
            tts_response = await add_voice_to_tts_api(
                str(voice.user_id),
                voice.voice_name,
                file,
                original_filename,
                content_type,
            )

        # Update voice status and processed file path
        voice.status = VoiceStatus.READY.value
        voice.processed_file_path = ",".join(tts_response.get("parts", []))

        # Update additional fields from TTS API response
        voice.total_length = tts_response.get("total_length")
        # Add any other fields from the TTS API response that you want to store

        db.commit()
        print(f"Voice processing completed for voice id {voice_id}")
    except Exception as e:
        # If any error occurs during processing, update status to failed
        voice.status = VoiceStatus.FAILED.value
        db.commit()
        print(f"Voice processing failed for voice id {voice_id}: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def get_correct_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        # If we can't guess, default to a common audio type
        return "audio/mpeg"
    return mime_type


async def add_voice_to_tts_api(
    user_id: str, voice_name: str, file, original_filename: str, content_type: str
):
    async with aiohttp.ClientSession() as session:
        url = f"{TTS_API_URL}/add_voice"
        data = aiohttp.FormData()
        data.add_field("user_id", user_id)
        data.add_field("voice_name", voice_name)

        # Use the correct MIME type
        correct_content_type = get_correct_mime_type(original_filename)
        data.add_field(
            "file", file, filename=original_filename, content_type=correct_content_type
        )

        async with session.post(url, data=data) as response:
            response_text = await response.text()
            print(f"TTS API Response: {response.status} - {response_text}")
            if response.status != 201:
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to add voice to TTS API: {response_text}",
                )
            return await response.json()


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
            total_length=voice.total_length,
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
        .filter(
            ((Voice.user_id == user_id) | (Voice.is_default == True))
            & (Voice.status == "READY")
        )
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
            total_length=voice.total_length,
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
        total_length=voice.total_length,
        created_at=voice.created_at,
        updated_at=voice.updated_at,
    )


async def delete_voice(db: Session, user_id: int, voice_id: int) -> dict:
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

    # Delete the voice from the TTS API
    await delete_voice_from_tts_api(user_id, voice.voice_name)

    db.delete(voice)
    db.commit()
    return {"message": f"Voice with id {voice_id} has been successfully deleted"}


async def delete_voice_from_tts_api(user_id: int, voice_name: str):
    async with aiohttp.ClientSession() as session:
        url = f"{TTS_API_URL}/delete_voice/{user_id}/{voice_name}"
        async with session.delete(url) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to delete voice from TTS API: {await response.text()}",
                )


def create_default_voices(db: Session, base_path: str) -> list[VoiceResponse]:
    default_voices = [
        {"voice_name": "default_en_male", "language": "en", "gender": "male"},
        {"voice_name": "default_en_female", "language": "en", "gender": "female"},
        {"voice_name": "default_vi_male", "language": "vi", "gender": "male"},
        {"voice_name": "default_vi_female", "language": "vi", "gender": "female"},
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
                status=VoiceStatus.READY,
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
            total_length=voice.total_length,
            created_at=voice.created_at,
            updated_at=voice.updated_at,
        )
        for voice in created_voices
    ]
