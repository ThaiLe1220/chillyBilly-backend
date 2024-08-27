""" ./backend/services/audio_service.py"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from models import Audio, TextEntry, Voice
from schemas.audio import AudioCreate, AudioResponse
from models.voice import VoiceStatus
from models.audio import AudioStatus
from typing import List, Optional
import asyncio
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
    else:
        print("Voice found: ", voice.voice_name, voice.id, voice.status)

    if text_entry.guest_id is not None:
        raise HTTPException(status_code=403, detail="Guests cannot use custom voices")

    if voice.user_id != text_entry.user_id and not voice.is_default:
        raise HTTPException(status_code=403, detail="Cannot use another user's voice")

    # Check if voice is ready
    if voice.status != VoiceStatus.READY:
        raise HTTPException(status_code=400, detail="Voice is not ready for use")

    # Create initial empty audio entry
    db_audio = Audio(
        text_entry_id=audio.text_entry_id,
        voice_id=voice_id,
        user_id=text_entry.user_id,
        guest_id=text_entry.guest_id,
        status=AudioStatus.CREATED,
    )

    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)

    # Start background task
    background_tasks.add_task(
        process_audio, db, db_audio.id, audio.text_entry_id, voice_id
    )

    return AudioResponse(
        id=db_audio.id,
        text_entry_id=db_audio.text_entry_id,
        voice_id=db_audio.voice_id,
        status=db_audio.status,
        created_at=db_audio.created_at,
        updated_at=db_audio.updated_at,
    )


async def process_audio(db: Session, audio_id: int, text_entry_id: int, voice_id: int):
    # Fetch fresh instances of TextEntry and Voice within this function
    text_entry = db.query(TextEntry).filter(TextEntry.id == text_entry_id).first()
    voice = db.query(Voice).filter(Voice.id == voice_id).first()

    if not text_entry or not voice:
        print(f"Text entry or voice not found for audio {audio_id}")
        return

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

    max_retries = 500
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TTS_API_URL}/generate_audio", json=tts_data, timeout=30.0
                )
                response.raise_for_status()
                tts_result = response.json()

            # Update the audio object with the results from the TTS API
            db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
            if db_audio:
                db_audio.audio_path = tts_result.get("audio_path", "")
                db_audio.audio_duration = tts_result.get("audio_duration", 0)
                db_audio.audio_size = tts_result.get("audio_size", 0)
                db_audio.status = AudioStatus.READY
                db_audio.mime_type = tts_result.get("mime_type", "")
                db_audio.sample_rate = tts_result.get("sample_rate", 0)
                db_audio.file_url = tts_result.get("file_url", "")
                db_audio.delete_url = tts_result.get("delete_url", "")
                db_audio.audio_name = tts_result.get("audio_name", "")
                db_audio.generation_time = tts_result.get("generation_time", 0)
                db_audio.language = tts_result.get("language", "")
                db_audio.preset = tts_result.get("preset", "")
                db_audio.text_length = tts_result.get("text_length", 0)
                db_audio.voice_name = tts_result.get("voice_name", "")

                db.commit()
            break  # Exit the loop if successful

        except httpx.HTTPStatusError as e:
            print(
                f"Attempt {attempt + 1} failed for audio {audio_id}: HTTP {e.response.status_code}"
            )
            print(f"Response content: {e.response.text}")
            if e.response.status_code == 404:
                print(
                    "Voice not found. Please check if the voice exists in the TTS API."
                )
                break  # Exit the retry loop if voice is not found
            if attempt == max_retries - 1:
                # Update status to FAILED if all retries are exhausted
                db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
                if db_audio:
                    db_audio.status = AudioStatus.FAILED
                    db.commit()
                print(f"All retries failed for audio {audio_id}: {str(e)}")
            else:
                await asyncio.sleep(retry_delay)
        except httpx.RequestError as e:
            print(f"Attempt {attempt + 1} failed for audio {audio_id}: {str(e)}")
            if attempt == max_retries - 1:
                # Update status to FAILED if all retries are exhausted
                db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
                if db_audio:
                    db_audio.status = AudioStatus.FAILED
                    db.commit()
                print(f"All retries failed for audio {audio_id}: {str(e)}")
            else:
                await asyncio.sleep(retry_delay)


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
