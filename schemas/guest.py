""" ./schemas/guest.py"""

from pydantic import BaseModel, Field
from datetime import datetime


class GuestResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the guest", example=1)
    created_at: datetime = Field(
        ...,
        description="The timestamp when the guest was created",
        example="2024-07-10T03:29:24.910547",
    )
    last_active_date: datetime = Field(
        ...,
        description="The timestamp of the guest's last activity",
        example="2024-07-10T04:15:55.319846",
    )
    expiration_date: datetime = Field(
        ...,
        description="The timestamp of the guest's expiration date",
        example="2024-08-10T04:15:55.319846",
    )

    class Config:
        from_attributes = True
