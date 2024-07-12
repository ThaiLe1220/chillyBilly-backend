""" ./services/audio_service.py"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Audio, TextEntry, Voice
from schemas.audio import AudioCreate, AudioResponse
import random
import os


def create_audio(db: Session, audio: AudioCreate) -> AudioResponse:
    text_entry = db.query(TextEntry).filter(TextEntry.id == audio.text_entry_id).first()
    if not text_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Text entry not found"
        )

    if audio.voice_id:
        voice = db.query(Voice).filter(Voice.id == audio.voice_id).first()
        if not voice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Voice not found"
            )

        if text_entry.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Guests cannot use custom voices",
            )

        if voice.user_id != text_entry.user_id and not voice.is_default:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot use another user's voice",
            )

    db_audio = Audio(**audio.dict())
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


def get_audio(db: Session, audio_id: int) -> AudioResponse:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )
    return db_audio


def delete_audio(db: Session, audio_id: int) -> int:
    db_audio = db.query(Audio).filter(Audio.id == audio_id).first()
    if db_audio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )
    db.delete(db_audio)
    db.commit()
    return audio_id


def generate_audio(db: Session, text_entry_id: int, voice_id: int = None):
    text_entry = db.query(TextEntry).filter(TextEntry.id == text_entry_id).first()
    if not text_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Text entry not found"
        )

    if voice_id:
        voice_clone = db.query(Voice).filter(Voice.id == voice_id).first()
        if not voice_clone:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Voice clone not found"
            )

        if text_entry.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Guests cannot use custom voices",
            )

        if voice_clone.user_id != text_entry.user_id and not voice_clone.is_default:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot use another user's voice clone",
            )

    # Mock TTS generation process
    audio_dir = "/path/to/generated/audio"
    os.makedirs(audio_dir, exist_ok=True)
    file_name = f"audio_{text_entry_id}_{random.randint(1000, 9999)}.mp3"
    file_path = os.path.join(audio_dir, file_name)

    # Create an empty file to simulate audio generation
    with open(file_path, "w") as f:
        pass

    # Generate a random duration between 5 and 20 seconds
    duration = round(random.uniform(5, 20), 2)

    audio = Audio(
        text_entry_id=text_entry_id,
        voice_id=voice_id,
        file_path=file_path,
        duration=duration,
        user_id=text_entry.user_id,
        guest_id=text_entry.guest_id,
    )
    db.add(audio)
    db.commit()
    db.refresh(audio)

    return AudioResponse(
        id=audio.id,
        text_entry_id=audio.text_entry_id,
        voice_id=audio.voice_id,
        file_path=audio.file_path,
        duration=audio.duration,
        created_at=audio.created_at,
    )
