""" ./backend/schemas/tab.py"""


from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TabCreate(BaseModel):
    user_id: Optional[int] = Field(None, description="The user's ID if applicable")
    guest_id: Optional[int] = Field(None, description="The guest's ID if applicable")
    tab_name: str = Field(..., description="Name of the tab")


class TabUpdate(BaseModel):
    user_id: Optional[int] = Field(None, description="ID of the user who owns the tab", example=1)
    guest_id: Optional[int] = Field(None, description="ID of the guest associated with the tab", example=2)
    tab_name: Optional[str] = Field(None, description="Name of the tab", example="Updated Tab Name")

    class Config:
        from_attributes = True


class  TabResponse(BaseModel):
    id: int = Field(..., description="The unique identifier for the tab", example=1)
    tab_name: str = Field(..., description="Name of the tab", example="Sample Tab")

    class Config:
        from_attributes = True