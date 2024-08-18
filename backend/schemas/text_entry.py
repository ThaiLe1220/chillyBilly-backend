""" ./backend/schemas/text_entry.py"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TextEntryCreate(BaseModel):
    content: str = Field(..., description="The content of the text entry", example="Hello, world!")
    language: Optional[str] = Field(..., description="The language of the text entry", example="en")
    user_id: Optional[int] = Field(None, description="The user's ID if applicable")
    guest_id: Optional[int] = Field(None, description="The guest's ID if applicable")
    tab_generation_id: int = Field(..., description="The ID of the associated tab generation")



class TextEntryResponse(BaseModel):
    id: int = Field(..., description="The text entry's unique identifier", example=1)
    content: str = Field(
        ..., description="The content of the text entry", example="Hello, world!"
    )
    language: str = Field(
        ..., description="The language of the text entry", example="en"
    )
    created_at: datetime = Field(
        ...,
        description="The creation timestamp of the text entry",
        example="2024-01-01T00:00:00",
    )

    class Config:
        from_attributes = True
