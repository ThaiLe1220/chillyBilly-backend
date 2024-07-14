""" ./backend/models/user.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    UniqueConstraint,
    Enum,
)
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class UserRole(PyEnum):
    ADMIN = "ADMIN"
    REGULAR = "REGULAR"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    two_factor_enabled = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.REGULAR, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    last_active_date = Column(DateTime, nullable=True)

    user_profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    text_entry = relationship(
        "TextEntry", back_populates="user", cascade="all, delete-orphan"
    )
    audio = relationship("Audio", back_populates="user", cascade="all, delete-orphan")
    voice = relationship(
        "Voice",
        back_populates="user",
        cascade="all, delete-orphan",
        primaryjoin="and_(User.id==Voice.user_id, Voice.is_default==False)",
    )
    user_feedback = relationship(
        "UserFeedback", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("email", name="uq_email"),
    )
