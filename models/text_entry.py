""" ./models/text_entry.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class TextEntry(Base):
    __tablename__ = "text_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    guest_id = Column(
        Integer, ForeignKey("guests.id", ondelete="CASCADE"), nullable=True
    )
    content = Column(Text, nullable=False)
    language = Column(Enum("vi", "en", name="language_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="text_entries")
    guest = relationship("Guest", back_populates="text_entries")
    generated_audio = relationship(
        "GeneratedAudio", back_populates="text_entry", cascade="all, delete"
    )

    __table_args__ = (
        CheckConstraint(
            "(user_id IS NULL) != (guest_id IS NULL)", name="check_user_xor_guest"
        ),
    )
