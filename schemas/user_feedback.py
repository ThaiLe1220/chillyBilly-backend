""" ./schemas/feedback.py"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserFeedbackCreate(BaseModel):
    audio_id: int
    rating: int
    comment: Optional[str] = None


class UserFeedbackUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class UserFeedbackResponse(BaseModel):
    id: int
    user_id: int
    audio_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
