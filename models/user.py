""" ./models/user.py"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
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
    last_login = Column(DateTime, nullable=True)
    last_active_date = Column(DateTime, nullable=True)

    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    text_entries = relationship(
        "TextEntry", back_populates="user", cascade="all, delete"
    )
    generated_audio = relationship(
        "GeneratedAudio", back_populates="user", cascade="all, delete"
    )
    voice_clones = relationship(
        "VoiceClone",
        back_populates="user",
        cascade="all, delete",
        primaryjoin="and_(User.id==VoiceClone.user_id, VoiceClone.is_default==False)",
    )
    user_feedback = relationship(
        "UserFeedback", back_populates="user", cascade="all, delete"
    )
    # sessions = relationship(
    #     "Session", back_populates="user", cascade="all, delete-orphan"
    # )
    # usage_history = relationship(
    #     "UsageHistory", back_populates="user", cascade="all, delete-orphan"
    # )
    # api_usage = relationship(
    #     "APIUsage", back_populates="user", cascade="all, delete-orphan"
    # )

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )
