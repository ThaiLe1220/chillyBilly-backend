""" ./models/user.py"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    two_factor_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_active_date = Column(DateTime, nullable=True)

    user_profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    text_entry = relationship("TextEntry", back_populates="user", cascade="all, delete")
    audio = relationship("Audio", back_populates="user", cascade="all, delete")
    voice = relationship(
        "Voice",
        back_populates="user",
        cascade="all, delete",
        primaryjoin="and_(User.id==Voice.user_id, Voice.is_default==False)",
    )
    user_feedback = relationship(
        "UserFeedback", back_populates="user", cascade="all, delete"
    )

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )
