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
    tab_generation_id: int = Field(
        ..., description="The ID of the associated tab generation"
    )


class AudioResponse(BaseModel):
    id: int = Field(..., description="The generated audio's unique identifier")
    text_entry_id: int = Field(..., description="The ID of the associated text entry")
    voice_id: Optional[int] = Field(
        None, description="The ID of the voice used (if any)"
    )
    audio_path: str = Field(..., description="The path to the generated audio file")
    audio_duration: Optional[float] = Field(
        None, description="The duration of the audio in seconds"
    )
    audio_size: Optional[int] = Field(
        None, description="The size of the audio file in bytes"
    )
    status: AudioStatus = Field(..., description="The current status of the audio")
    created_at: datetime = Field(
        ..., description="The creation timestamp of the generated audio"
    )
    updated_at: datetime = Field(
        ..., description="The last update timestamp of the generated audio"
    )
    mime_type: Optional[str] = Field(
        None, description="The MIME type of the audio file"
    )
    sample_rate: Optional[int] = Field(
        None, description="The sample rate of the audio file"
    )
    file_url: Optional[str] = Field(
        None, description="The URL to download the audio file"
    )
    delete_url: Optional[str] = Field(
        None, description="The URL to delete the audio file"
    )
    audio_name: Optional[str] = Field(
        None, description="The name of the generated audio file"
    )
    generation_time: Optional[float] = Field(
        None, description="The time taken to generate the audio"
    )
    language: Optional[str] = Field(
        None, description="The language of the generated audio"
    )
    preset: Optional[str] = Field(
        None, description="The preset used for audio generation"
    )
    text_length: Optional[int] = Field(None, description="The length of the input text")
    voice_name: Optional[str] = Field(None, description="The name of the voice used")

    @validator("audio_duration")
    @classmethod
    def audio_duration_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Audio duration must be positive")
        return v

    @validator("audio_size")
    @classmethod
    def audio_size_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Audio size must be positive")
        return v

    @validator("sample_rate")
    @classmethod
    def sample_rate_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Sample rate must be positive")
        return v

    @validator("generation_time")
    @classmethod
    def generation_time_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Generation time must be positive")
        return v

    @validator("text_length")
    @classmethod
    def text_length_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Text length must be positive")
        return v

    class Config:
        from_attributes = True
