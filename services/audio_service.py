""" ./services/audio_service.py"""

import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from models import Audio, TextEntry, Voice
from schemas.audio import AudioCreate, AudioResponse, AudioStatus
from typing import List, Optional
from database import SessionLocal  # Import your database session creator


def create_audio(
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

    # Create the audio object with user_id and guest_id from the text entry
    db_audio = Audio(
        text_entry_id=audio.text_entry_id,
        voice_id=voice_id,
        file_path=audio.file_path,
        duration=audio.duration,
        file_size=audio.file_size,
        user_id=text_entry.user_id,
        guest_id=text_entry.guest_id,
        status=AudioStatus.PROCESSING,
    )

    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)

    # Start audio processing in the background
    background_tasks.add_task(process_audio, db_audio.id)

    return AudioResponse(
        id=db_audio.id,
        text_entry_id=db_audio.text_entry_id,
        voice_id=db_audio.voice_id,
        file_path=db_audio.file_path,
        duration=db_audio.duration,
        file_size=db_audio.file_size,
        status=db_audio.status.value,
        created_at=db_audio.created_at,
        updated_at=db_audio.updated_at,
    )


async def process_audio(audio_id: int):
    # Create a new database session for this background task
    db = SessionLocal()
    try:
        audio = db.query(Audio).filter(Audio.id == audio_id).first()
        if not audio:
            print(f"Audio with id {audio_id} not found")
            return

        # Wait for 10 seconds (simulating audio processing)
        await asyncio.sleep(10)

        # Update audio status
        audio.status = AudioStatus.READY
        db.commit()
        print(f"Audio processing completed for audio id {audio_id}")

    except Exception as e:
        # If any error occurs during processing, update status to failed
        audio.status = AudioStatus.FAILED
        db.commit()
        print(f"Audio processing failed for audio id {audio_id}: {str(e)}")
    finally:
        db.close()


def get_audio(db: Session, audio_id: int) -> AudioResponse:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return AudioResponse(
        id=db_audio.id,
        text_entry_id=db_audio.text_entry_id,
        voice_id=db_audio.voice_id,
        file_path=db_audio.file_path,
        duration=db_audio.duration,
        file_size=db_audio.file_size,
        status=db_audio.status.value,
        created_at=db_audio.created_at,
        updated_at=db_audio.updated_at,
    )


def get_audios(
    db: Session, user_id: Optional[int] = None, guest_id: Optional[int] = None
) -> List[AudioResponse]:
    query = db.query(Audio)
    if user_id is not None:
        query = query.filter(Audio.user_id == user_id)
    elif guest_id is not None:
        query = query.filter(Audio.guest_id == guest_id)
    db_audios = query.all()
    return [
        AudioResponse(
            id=audio.id,
            text_entry_id=audio.text_entry_id,
            voice_id=audio.voice_id,
            file_path=audio.file_path,
            duration=audio.duration,
            file_size=audio.file_size,
            status=audio.status.value,
            created_at=audio.created_at,
            updated_at=audio.updated_at,
        )
        for audio in db_audios
    ]


def get_all_audios(db: Session) -> List[AudioResponse]:
    db_audios = db.query(Audio).all()
    return [
        AudioResponse(
            id=audio.id,
            text_entry_id=audio.text_entry_id,
            voice_id=audio.voice_id,
            file_path=audio.file_path,
            duration=audio.duration,
            file_size=audio.file_size,
            status=audio.status.value,
            created_at=audio.created_at,
            updated_at=audio.updated_at,
        )
        for audio in db_audios
    ]


def delete_audio(db: Session, audio_id: int) -> int:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    db.delete(db_audio)
    db.commit()
    return audio_id
