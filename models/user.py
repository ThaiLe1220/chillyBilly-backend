"""Filename: ./models/user.py"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    two_factor_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    last_active_date = Column(DateTime)

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    text_entries = relationship(
        "TextEntry", back_populates="user", cascade="all, delete-orphan"
    )
    # generated_audio = relationship(
    #     "GeneratedAudio", back_populates="user", cascade="all, delete-orphan"
    # )
    # voice_clones = relationship(
    #     "VoiceClone", back_populates="user", cascade="all, delete-orphan"
    # )
    # sessions = relationship(
    #     "Session", back_populates="user", cascade="all, delete-orphan"
    # )
    # usage_history = relationship(
    #     "UsageHistory", back_populates="user", cascade="all, delete-orphan"
    # )
    # api_usage = relationship(
    #     "APIUsage", back_populates="user", cascade="all, delete-orphan"
    # )
    # user_feedback = relationship(
    #     "UserFeedback", back_populates="user", cascade="all, delete-orphan"
    # )
