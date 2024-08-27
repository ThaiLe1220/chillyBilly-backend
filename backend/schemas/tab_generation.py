""" ./backend/schemas/tab_generation.py"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from models import Audio
from schemas.audio import AudioResponse


class TabGenerationBase(BaseModel):
    tab_id: int = Field(..., description="ID of the associated tab")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the tab generation was created"
    )


class TabGenerationCreate(TabGenerationBase):
    text_entry_content: Optional[str] = Field(
        None, description="Content for the associated text entry"
    )
    language: str = Field(
        ..., description="The language of the text entry", example="en"
    )
    voice_id: int = Field(..., description="ID of the voice")


class TabGenerationResponse(TabGenerationBase):
    id: int = Field(..., description="Unique identifier of the tab generation")
    text_entry_content: Optional[str] = Field(
        None, description="Content of the associated text entry"
    )
    audio: Optional[AudioResponse] = Field(None, description="The audio")

    class Config:
        from_attributes = True
