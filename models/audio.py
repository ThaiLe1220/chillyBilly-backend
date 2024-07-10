""" ./models/audio.py"""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class TextEntry(Base):
    __tablename__ = "text_entries"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)
    owner_type = Column(Enum("user", "guest", name="owner_type_enum"), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(Enum("vi", "en", name="language_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="text_entries",
        primaryjoin="and_(TextEntry.owner_id==User.id, TextEntry.owner_type=='user')",
    )
    guest = relationship(
        "Guest",
        back_populates="text_entries",
        primaryjoin="and_(TextEntry.owner_id==Guest.id, TextEntry.owner_type=='guest')",
    )
    generated_audio = relationship(
        "GeneratedAudio", back_populates="text_entry", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_owner", "owner_id", "owner_type"),)
