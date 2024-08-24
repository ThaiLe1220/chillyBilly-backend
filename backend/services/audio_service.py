""" ./backend/services/audio_service.py"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from models import Audio, TextEntry, Voice
from schemas.audio import AudioCreate, AudioResponse, AudioStatus
from typing import List, Optional
import httpx
import os


TTS_API_URL = os.getenv("TTS_API_URL", "http://localhost:8080")


async def create_audio(
    db: Session, audio: AudioCreate, background_tasks: BackgroundTasks
) -> AudioResponse:
    text_entry = db.query(TextEntry).filter(TextEntry.id == audio.text_entry_id).first()
    if not text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")

    # Use provided voice_id if present, otherwise determine based on language
    if audio.voice_id is not None:
        voice_id = audio.voice_id
    else:
        if text_entry.language == "vi":
            voice_id = 1
        elif text_entry.language == "en":
            voice_id = 3
        else:
            raise HTTPException(status_code=400, detail="Unsupported language")

    voice = db.query(Voice).filter(Voice.id == voice_id).first()
    if not voice:
        raise HTTPException(status_code=404, detail="Voice not found")

    if text_entry.guest_id is not None:
        raise HTTPException(status_code=403, detail="Guests cannot use custom voices")

    if voice.user_id != text_entry.user_id and not voice.is_default:
        raise HTTPException(status_code=403, detail="Cannot use another user's voice")

    # Check if voice is ready
    if voice.status != "ready":
        raise HTTPException(status_code=400, detail="Voice is not ready for use")

    # Prepare data for local TTS API
    tts_data = {
        "text": text_entry.content,
        "lang": text_entry.language,
        "voice_name": voice.voice_name,
        "user_id": (
            str(text_entry.user_id) if text_entry.user_id else str(text_entry.guest_id)
        ),
        "user_type": "user" if text_entry.user_id else "guest",
        "preset": "ultra_fast",
    }

    print(f"[create_audio] tts_data: {tts_data}")

    try:
        # Call local TTS API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TTS_API_URL}/generate_audio", json=tts_data, timeout=30.0
            )
            response.raise_for_status()
            tts_result = response.json()

        # Create the audio object with the results from the TTS API
        db_audio = Audio(
            text_entry_id=audio.text_entry_id,
            voice_id=voice_id,
            audio_path=tts_result.get("audio_path", ""),
            audio_duration=tts_result.get("audio_duration", 0),
            audio_size=tts_result.get("audio_size", 0),
            user_id=text_entry.user_id,
            guest_id=text_entry.guest_id,
            status=AudioStatus.READY,
            mime_type=tts_result.get("mime_type", ""),
            sample_rate=tts_result.get("sample_rate", 0),
            file_url=tts_result.get("file_url", ""),
            delete_url=tts_result.get("delete_url", ""),
            audio_name=tts_result.get("audio_name", ""),
            generation_time=tts_result.get("generation_time", 0),
            language=tts_result.get("language", ""),
            preset=tts_result.get("preset", ""),
            text_length=tts_result.get("text_length", 0),
            voice_name=tts_result.get("voice_name", ""),
            tab_generation_id=audio.tab_generation_id,
        )

        db.add(db_audio)
        db.commit()
        db.refresh(db_audio)

        return AudioResponse(
            id=db_audio.id,
            text_entry_id=db_audio.text_entry_id,
            voice_id=db_audio.voice_id,
            audio_path=db_audio.audio_path,
            audio_duration=db_audio.audio_duration,
            audio_size=db_audio.audio_size,
            status=db_audio.status,
            created_at=db_audio.created_at,
            updated_at=db_audio.updated_at,
            mime_type=db_audio.mime_type,
            sample_rate=db_audio.sample_rate,
            file_url=db_audio.file_url,
            delete_url=db_audio.delete_url,
            audio_name=db_audio.audio_name,
            generation_time=db_audio.generation_time,
            language=db_audio.language,
            preset=db_audio.preset,
            text_length=db_audio.text_length,
            voice_name=db_audio.voice_name,
        )

    except httpx.HTTPError as e:
        # Handle HTTP errors from the TTS API
        error_detail = f"TTS API error: {str(e)}"
        print(error_detail)  # Log the error
        db_audio = Audio(
            text_entry_id=audio.text_entry_id,
            voice_id=voice_id,
            audio_path="error",
            user_id=text_entry.user_id,
            guest_id=text_entry.guest_id,
            status=AudioStatus.FAILED,
        )
        db.add(db_audio)
        db.commit()
        db.refresh(db_audio)
        raise HTTPException(status_code=500, detail=error_detail) from e

    except Exception as e:
        # Handle other exceptions
        error_detail = f"Unexpected error during audio processing: {str(e)}"
        print(error_detail)  # Log the error
        db_audio = Audio(
            text_entry_id=audio.text_entry_id,
            voice_id=voice_id,
            audio_path="error",
            user_id=text_entry.user_id,
            guest_id=text_entry.guest_id,
            status=AudioStatus.FAILED,
        )
        db.add(db_audio)
        db.commit()
        db.refresh(db_audio)
        raise HTTPException(status_code=500, detail=error_detail) from e


async def get_audio(db: Session, audio_id: int) -> AudioResponse:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return AudioResponse(
        id=db_audio.id,
        text_entry_id=db_audio.text_entry_id,
        voice_id=db_audio.voice_id,
        audio_path=db_audio.audio_path,
        audio_duration=db_audio.audio_duration,
        audio_size=db_audio.audio_size,
        status=db_audio.status,
        created_at=db_audio.created_at,
        updated_at=db_audio.updated_at,
        mime_type=db_audio.mime_type,
        sample_rate=db_audio.sample_rate,
        file_url=db_audio.file_url,
        delete_url=db_audio.delete_url,
        audio_name=db_audio.audio_name,
        generation_time=db_audio.generation_time,
        language=db_audio.language,
        preset=db_audio.preset,
        text_length=db_audio.text_length,
        voice_name=db_audio.voice_name,
    )


async def get_audios(
    db: Session,
    user_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    status: Optional[AudioStatus] = None,
) -> List[AudioResponse]:
    query = db.query(Audio)
    if user_id is not None:
        query = query.filter(Audio.user_id == user_id)
    if guest_id is not None:
        query = query.filter(Audio.guest_id == guest_id)
    if status is not None:
        query = query.filter(Audio.status == status)
    db_audios = query.all()
    return [
        AudioResponse(
            id=audio.id,
            text_entry_id=audio.text_entry_id,
            voice_id=audio.voice_id,
            audio_path=audio.audio_path,
            audio_duration=audio.audio_duration,
            audio_size=audio.audio_size,
            status=audio.status,
            created_at=audio.created_at,
            updated_at=audio.updated_at,
            mime_type=audio.mime_type,
            sample_rate=audio.sample_rate,
            file_url=audio.file_url,
            delete_url=audio.delete_url,
            audio_name=audio.audio_name,
            generation_time=audio.generation_time,
            language=audio.language,
            preset=audio.preset,
            text_length=audio.text_length,
            voice_name=audio.voice_name,
        )
        for audio in db_audios
    ]


async def get_all_audios(
    db: Session,
    user_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    status: Optional[AudioStatus] = None,
) -> List[AudioResponse]:
    query = db.query(Audio)
    if user_id is not None:
        query = query.filter(Audio.user_id == user_id)
    if guest_id is not None:
        query = query.filter(Audio.guest_id == guest_id)
    if status is not None:
        query = query.filter(Audio.status == status)
    db_audios = query.all()
    return [
        AudioResponse(
            id=audio.id,
            text_entry_id=audio.text_entry_id,
            voice_id=audio.voice_id,
            audio_path=audio.audio_path,
            audio_duration=audio.audio_duration,
            audio_size=audio.audio_size,
            status=audio.status,
            created_at=audio.created_at,
            updated_at=audio.updated_at,
            mime_type=audio.mime_type,
            sample_rate=audio.sample_rate,
            file_url=audio.file_url,
            delete_url=audio.delete_url,
            audio_name=audio.audio_name,
            generation_time=audio.generation_time,
            language=audio.language,
            preset=audio.preset,
            text_length=audio.text_length,
            voice_name=audio.voice_name,
        )
        for audio in db_audios
    ]


async def delete_audio(db: Session, audio_id: int) -> int:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")

    # Delete the audio file using the delete_url
    async with httpx.AsyncClient() as client:
        response = await client.delete(db_audio.delete_url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Failed to delete audio file from storage"
            )

    db.delete(db_audio)
    db.commit()
    return audio_id
