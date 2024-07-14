""" ./backend/schemas/user_feedback.py """

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserFeedbackCreate(BaseModel):
    audio_id: int = Field(..., description="Unique identifier for the audio content.")
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating given by the user, ranging from 1 (lowest) to 5 (highest).",
    )
    comment: Optional[str] = Field(
        None, description="Optional comment provided by the user for feedback."
    )


class UserFeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Updated rating given by the user, ranging from 1 (lowest) to 5 (highest).",
    )
    comment: Optional[str] = Field(
        None, description="Updated optional comment provided by the user for feedback."
    )


class UserFeedbackResponse(BaseModel):
    id: int = Field(..., description="Unique identifier for the feedback entry.")
    user_id: int = Field(
        ..., description="Unique identifier for the user who provided the feedback."
    )
    audio_id: int = Field(..., description="Unique identifier for the audio content.")
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating given by the user, ranging from 1 (lowest) to 5 (highest).",
    )
    comment: Optional[str] = Field(
        None, description="Optional comment provided by the user for feedback."
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the feedback was created."
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the feedback was last updated."
    )

    class Config:
        from_attributes = True
