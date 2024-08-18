""" ./backend/models/tab_generation.py"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    Enum,
)

from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from enum import Enum as PyEnum

class TabGeneration(Base):
    __tablename__ = "tab_generation"

    id = Column(Integer, primary_key=True, index=True)
    tab_id = Column(Integer, ForeignKey("tab.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tab = relationship("Tab", back_populates="tab_generation")
    text_entry = relationship("TextEntry", back_populates="tab_generation")
    audio = relationship("Audio", back_populates="tab_generation")