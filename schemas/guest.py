""" ./schemas/guest.py"""

from pydantic import BaseModel, Field
from datetime import datetime


class GuestCreate(BaseModel):
    guest_id: str = Field(..., description="Unique identifier for the guest")


class GuestResponse(BaseModel):
    id: int
    guest_id: str
    created_at: datetime
    last_active_date: datetime

    class Config:
        from_attributes = True
