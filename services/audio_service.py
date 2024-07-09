""" ./services/audio_service.py"""

from models import TextEntry, VoiceClone, GeneratedAudio
from sqlalchemy.orm import Session


def generate_audio(db: Session, text_entry_id: int, voice_clone_id: int = None):
    text_entry = db.query(TextEntry).filter(TextEntry.id == text_entry_id).first()
    if not text_entry:
        raise ValueError("Text entry not found")

    voice_clone = None
    if voice_clone_id:
        voice_clone = (
            db.query(VoiceClone).filter(VoiceClone.id == voice_clone_id).first()
        )
        if not voice_clone:
            raise ValueError("Voice clone not found")

    # Here, implement the actual TTS generation process
    # This is a placeholder for the actual implementation
    file_path = f"/path/to/generated/audio_{text_entry_id}.mp3"
    duration = 10.5  # placeholder duration

    audio = GeneratedAudio(
        text_entry_id=text_entry_id,
        voice_clone_id=voice_clone_id,
        file_path=file_path,
        duration=duration,
    )
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio
