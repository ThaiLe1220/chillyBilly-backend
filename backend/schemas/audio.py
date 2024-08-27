""" ./backend/schemas/audio.py"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum


class AudioStatus(str, Enum):
    CREATED = "CREATED"
    READY = "READY"
    FAILED = "FAILED"


class AudioCreate(BaseModel):
    text_entry_id: int = Field(..., description="The ID of the associated text entry")
    voice_id: Optional[int] = Field(
        None, description="The ID of the voice to use (if any)"
    )
    tab_generation_id: int = Field(
        ..., description="The ID of the associated tab generation"
    )


class AudioResponse(BaseModel):
    id: int = Field(..., description="The generated audio's unique identifier")
    text_entry_id: int = Field(..., description="The ID of the associated text entry")

    voice_id: Optional[int] = Field(
        None, description="The ID of the voice used (if any)"
    )
    audio_duration: Optional[float] = Field(
        None, description="The duration of the audio in seconds"
    )
    audio_name: Optional[str] = Field(
        None, description="The name of the generated audio file"
    )
    audio_path: Optional[str] = Field(
        None, description="The path to the generated audio file"
    )
    audio_size: Optional[int] = Field(
        None, description="The size of the audio file in bytes"
    )
    audio_wavelength: Optional[float] = Field(
        None, description="The wavelength of the audio"
    )
    delete_url: Optional[str] = Field(
        None, description="The URL to delete the audio file"
    )
    download_url: Optional[str] = Field(
        None, description="The URL to download the audio file"
    )
    generation_time: Optional[float] = Field(
        None, description="The time taken to generate the audio in seconds"
    )
    language: Optional[str] = Field(
        None, description="The language of the generated audio"
    )
    message: Optional[str] = Field(
        None, description="A message about the audio generation process"
    )
    mime_type: Optional[str] = Field(
        None, description="The MIME type of the audio file"
    )
    preset: Optional[str] = Field(
        None, description="The preset used for audio generation"
    )
    sample_rate: Optional[int] = Field(
        None, description="The sample rate of the audio file"
    )
    text_length: Optional[int] = Field(None, description="The length of the input text")
    timestamp: Optional[int] = Field(
        None, description="The timestamp of audio generation"
    )
    voice_name: Optional[str] = Field(None, description="The name of the voice used")
    status: AudioStatus = Field(..., description="The current status of the audio")
    created_at: Optional[datetime] = Field(
        None, description="The creation timestamp of the generated audio"
    )
    updated_at: Optional[datetime] = Field(
        None, description="The last update timestamp of the generated audio"
    )

    class Config:
        from_attributes = True
