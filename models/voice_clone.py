""" ./models/voice_clone.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class VoiceClone(Base):
    __tablename__ = "voice_clones"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )  # Allow null for default voice clones
    voice_name = Column(String, nullable=False)
    original_file_path = Column(String, nullable=False)
    processed_file_path = Column(String)
    status = Column(
        Enum("processing", "ready", "failed", name="clone_status_enum"), nullable=False
    )
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="voice_clones")
    generated_audio = relationship("GeneratedAudio", back_populates="voice_clone")

    __table_args__ = (
        CheckConstraint(
            "(is_default = false) OR (is_default = true AND user_id IS NULL)"
        ),
    )
