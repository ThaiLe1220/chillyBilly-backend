""" ./backend/models/audio.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Enum,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from enum import Enum as PyEnum


class AudioStatus(PyEnum):
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class Audio(Base):
    __tablename__ = "audio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    guest_id = Column(Integer, ForeignKey("guest.id"), nullable=True, index=True)
    text_entry_id = Column(
        Integer, ForeignKey("text_entry.id"), nullable=False, index=True
    )
    voice_id = Column(Integer, ForeignKey("voice.id"), nullable=True)
    file_path = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)
    status = Column(Enum(AudioStatus), default=AudioStatus.PROCESSING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mime_type = Column(String, nullable=True)
    sample_rate = Column(Integer, nullable=True)
    file_url = Column(String, nullable=True)
    delete_url = Column(String, nullable=True)

    user = relationship("User", back_populates="audio")
    guest = relationship("Guest", back_populates="audio")
    text_entry = relationship("TextEntry", back_populates="audio")
    voice = relationship("Voice", back_populates="audio")
    user_feedback = relationship(
        "UserFeedback", back_populates="audio", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "(user_id IS NULL) != (guest_id IS NULL)", name="check_user_xor_guest"
        ),
    )
