""" ./models/audio.py"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class GeneratedAudio(Base):
    __tablename__ = "generated_audio"

    id = Column(Integer, primary_key=True, index=True)
    text_entry_id = Column(Integer, ForeignKey("text_entries.id"), nullable=False)
    voice_clone_id = Column(Integer, ForeignKey("voice_clones.id"), nullable=True)
    file_path = Column(String, nullable=False)
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    text_entry = relationship("TextEntry", back_populates="generated_audio")
    voice_clone = relationship("VoiceClone")
