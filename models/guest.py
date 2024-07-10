""" ./models/guest.py"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime)

    text_entries = relationship(
        "TextEntry", back_populates="guest", cascade="all, delete-orphan"
    )

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expiration_date

    def update_activity(self):
        self.last_active_date = datetime.utcnow()
        self.expiration_date = self.last_active_date + timedelta(
            days=30
        )  # Set expiration to 30 days from last activity
