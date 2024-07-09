"""Filename: ./schemas/user.py"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(
        ..., description="The user's chosen username", example="johndoe"
    )
    email: EmailStr = Field(
        ..., description="The user's email address", example="johndoe@example.com"
    )
    password: str = Field(
        ..., description="The user's password", example="SecurePassword123"
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", example="user@example.com"
    )
    password: Optional[str] = Field(
        None, description="The user's password", example="SecurePassword123"
    )

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int = Field(..., description="The user's unique identifier", example=1)
    username: str = Field(
        ..., description="The user's chosen username", example="johndoe"
    )
    email: EmailStr = Field(
        ..., description="The user's email address", example="johndoe@example.com"
    )
    created_at: datetime
    last_login: Optional[datetime]
    last_active_date: Optional[datetime]

    class Config:
        from_attributes = True
