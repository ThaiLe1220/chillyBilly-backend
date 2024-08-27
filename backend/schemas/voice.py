""" ./backend/schemas/voice.py"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from enum import Enum


class VoiceStatus(str, Enum):
    CREATED = "CREATED"
    READY = "READY"
    FAILED = "FAILED"


class VoiceCreate(BaseModel):
    voice_name: str = Field(..., max_length=100)
    original_file_path: str = Field(..., max_length=255)
    language: str = Field(..., pattern="^(en|vi)$")
    description: Optional[str] = None


class VoiceResponse(BaseModel):
    id: int
    user_id: Optional[int]
    voice_name: str
    original_file_path: str
    processed_file_path: Optional[str]
    status: VoiceStatus = Field(
        ..., description="The current status of the user uploaded voice"
    )
    is_default: bool
    language: str
    description: Optional[str]
    total_length: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VoiceUpdate(BaseModel):
    voice_name: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, pattern="^(en|vi)$")
    description: Optional[str] = None
    original_file_path: Optional[str] = Field(None, max_length=255)
