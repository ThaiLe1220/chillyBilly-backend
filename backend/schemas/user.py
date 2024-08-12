""" ./backend/schemas/user.py"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    REGULAR = "REGULAR"


class PasswordVerification(BaseModel):
    password: str


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
    role: UserRole = Field(default=UserRole.REGULAR, description="The user's role")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, description="The user's new username", example="newusername"
    )
    email: Optional[EmailStr] = Field(
        None, description="The user's email address", example="user@example.com"
    )
    password: Optional[str] = Field(
        None, description="The user's password", example="SecurePassword123"
    )
    is_active: Optional[bool] = Field(
        None, description="Whether the user account is active"
    )
    role: Optional[UserRole] = Field(None, description="The user's role")

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
    two_factor_enabled: bool = Field(
        ..., description="Whether two-factor authentication is enabled"
    )
    is_active: bool = Field(..., description="Whether the user account is active")
    role: UserRole = Field(..., description="The user's role")
    created_at: datetime = Field(
        ..., description="The date and time when the user was created"
    )
    updated_at: datetime = Field(
        ..., description="The date and time when the user was last updated"
    )
    last_login: Optional[datetime] = Field(
        None, description="The last login time of the user"
    )
    last_active_date: Optional[datetime] = Field(
        None, description="The last active date of the user"
    )

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Field(..., description="The user's username", example="johndoe")
    password: str = Field(
        ..., description="The user's password", example="SecurePassword123"
    )


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
