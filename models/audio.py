""" ./models/audio.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Audio(Base):
    __tablename__ = "audio"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    guest_id = Column(Integer, ForeignKey("guest.id"), nullable=True)
    text_entry_id = Column(Integer, ForeignKey("text_entry.id"), nullable=False)
    voice_id = Column(Integer, ForeignKey("voice.id"), nullable=True)
    file_path = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audio")
    guest = relationship("Guest", back_populates="audio")
    text_entry = relationship("TextEntry", back_populates="audio")
    voice = relationship("Voice", back_populates="audio")
    user_feedback = relationship(
        "UserFeedback", back_populates="audio", cascade="all, delete"
    )

    __table_args__ = (
        CheckConstraint(
            "(user_id IS NULL) != (guest_id IS NULL)", name="check_user_xor_guest"
        ),
    )
