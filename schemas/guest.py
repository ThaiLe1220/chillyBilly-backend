""" ./schemas/guest.py"""

from pydantic import BaseModel, Field
from datetime import datetime


class GuestResponse(BaseModel):
    id: int
    created_at: datetime
    last_active_date: datetime

    class Config:
        from_attributes = True
