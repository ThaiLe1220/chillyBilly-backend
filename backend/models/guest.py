""" ./backend/models/guest.py"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta


class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime)

    text_entry = relationship(
        "TextEntry", back_populates="guest", cascade="all, delete"
    )
    audio = relationship("Audio", back_populates="guest", cascade="all, delete")

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expiration_date

    def update_activity(self):
        self.last_active_date = datetime.utcnow()
        # self.expiration_date = self.last_active_date + timedelta(minutes=1)
        self.expiration_date = self.last_active_date + timedelta(days=7)
