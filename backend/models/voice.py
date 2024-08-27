""" ./backend/models/voice.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    CheckConstraint,
    Text,
    Float,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from enum import Enum as PyEnum


# implement this
class VoiceStatus(PyEnum):
    CREATED = "CREATED"
    READY = "READY"
    FAILED = "FAILED"


class Voice(Base):
    __tablename__ = "voice"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    voice_name = Column(String(100), nullable=False)
    original_file_path = Column(String(255), nullable=False)
    processed_file_path = Column(String(255))
    status = Column(Enum(VoiceStatus), default=VoiceStatus.CREATED, nullable=False)

    is_default = Column(Boolean, default=False)
    language = Column(Enum("en", "vi", name="voice_language_enum"), nullable=False)
    description = Column(Text)
    total_length = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="voice")
    audio = relationship("Audio", back_populates="voice")

    __table_args__ = (
        CheckConstraint(
            "(is_default = false) OR (is_default = true AND user_id IS NULL)"
        ),
        CheckConstraint("(is_default = true) OR (user_id IS NOT NULL)"),
    )
