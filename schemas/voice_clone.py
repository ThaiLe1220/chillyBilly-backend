""" ./schemas/voice_clone.py"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VoiceCloneCreate(BaseModel):
    voice_name: str
    original_file_path: str


class VoiceCloneResponse(BaseModel):
    id: int
    user_id: int
    voice_name: str
    original_file_path: str
    processed_file_path: Optional[str]
    status: str
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
