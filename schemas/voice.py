""" ./schemas/voice.py"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict


class VoiceCreate(BaseModel):
    voice_name: str = Field(..., max_length=100)
    original_file_path: str = Field(..., max_length=255)
    language: str = Field(..., regex="^(en|vi)$")
    description: Optional[str] = None


class VoiceResponse(BaseModel):
    id: int
    user_id: Optional[int]
    voice_name: str
    original_file_path: str
    processed_file_path: Optional[str]
    status: str
    is_default: bool
    language: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VoiceUpdate(BaseModel):
    voice_name: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, regex="^(en|vi)$")
    description: Optional[str] = None
    original_file_path: Optional[str] = Field(None, max_length=255)
