""" ./backend/models/tab.py"""

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


class Tab(Base):
    __tablename__ = "tab"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    guest_id = Column(Integer, ForeignKey("guest.id"), nullable=True, index=True)
    tab_name = Column(String, nullable=False)
    
    user = relationship("User", back_populates="tab")
    guest = relationship("Guest", back_populates="tab")
    tab_generation = relationship("TabGeneration", back_populates="tab", cascade="all, delete-orphan")
    
    