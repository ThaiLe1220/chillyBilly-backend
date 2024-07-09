""" ./schemas/profile.py"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfileCreate(BaseModel):
    first_name: str = Field(..., description="The user's first name", example="John")
    last_name: str = Field(..., description="The user's last name", example="Doe")
    date_of_birth: datetime = Field(
        ..., description="The user's date of birth", example="1990-01-01T00:00:00"
    )
    preferred_language: str = Field(
        ..., description="The user's preferred language", example="en"
    )


class UserProfileResponse(BaseModel):
    first_name: Optional[str] = Field(
        None, description="The user's first name", example="John"
    )
    last_name: Optional[str] = Field(
        None, description="The user's last name", example="Doe"
    )
    date_of_birth: Optional[datetime] = Field(
        None, description="The user's date of birth", example="1990-01-01T00:00:00"
    )
    preferred_language: Optional[str] = Field(
        None, description="The user's preferred language", example="en"
    )

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(
        None, description="The user's first name", example="John"
    )
    last_name: Optional[str] = Field(
        None, description="The user's last name", example="Doe"
    )
    date_of_birth: Optional[datetime] = Field(
        None, description="The user's date of birth", example="1990-01-01"
    )
    preferred_language: Optional[str] = Field(
        None, description="The user's preferred language", example="en"
    )

    class Config:
        from_attributes = True
