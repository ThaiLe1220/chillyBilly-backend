""" ./backend/schemas/audio.py"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum


class AudioStatus(str, Enum):
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class AudioCreate(BaseModel):
    text_entry_id: int = Field(..., description="The ID of the associated text entry")
    voice_id: Optional[int] = Field(
        None, description="The ID of the voice to use (if any)"
    )
    file_path: str = Field(..., description="The path to the generated audio file")
    duration: float = Field(..., description="The duration of the audio in seconds")
    file_size: Optional[int] = Field(
        None, description="The size of the audio file in bytes"
    )

    @validator("duration")
    @classmethod
    def duration_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Duration must be positive")
        return v

    @validator("file_size")
    @classmethod
    def file_size_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("File size must be positive")
        return v


class AudioResponse(BaseModel):
    id: int = Field(..., description="The generated audio's unique identifier")
    text_entry_id: int = Field(..., description="The ID of the associated text entry")
    voice_id: Optional[int] = Field(
        None, description="The ID of the voice used (if any)"
    )
    file_path: str = Field(..., description="The path to the generated audio file")
    duration: float = Field(..., description="The duration of the audio in seconds")
    file_size: Optional[int] = Field(
        None, description="The size of the audio file in bytes"
    )
    status: AudioStatus = Field(..., description="The current status of the audio")
    created_at: datetime = Field(
        ..., description="The creation timestamp of the generated audio"
    )
    updated_at: datetime = Field(
        ..., description="The last update timestamp of the generated audio"
    )

    class Config:
        from_attributes = True
