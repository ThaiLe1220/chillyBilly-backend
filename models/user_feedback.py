""" ./models/feedback.py"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    audio_id = Column(Integer, ForeignKey("audio.id"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_feedback")
    audio = relationship("Audio", back_populates="user_feedback")

    __table_args__ = (
        UniqueConstraint("user_id", "audio_id", name="uq_user_audio_feedback"),
    )
