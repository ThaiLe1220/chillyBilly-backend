""" ./backend/routers/tabs.py"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from services import tab_service
from schemas.tab import TabResponse, TabCreate, TabUpdateName
from database import get_db

router = APIRouter()


# Get all tabs by user_id
@router.get("/users/{user_id}/tabs", response_model=List[TabResponse])
def read_tabs_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tabs = tab_service.get_tabs_by_user_id(user_id, db)
    # if not tabs:
    #     raise HTTPException(status_code=404, detail="Tabs not found")
    return tabs


# Get a single tab by user_id and tab_id
@router.get("/users/{user_id}/tabs/{tab_id}", response_model=TabResponse)
def read_tab_by_user_id_and_tab_id(
    user_id: int, tab_id: int, db: Session = Depends(get_db)
):
    tab = tab_service.get_tab_by_user_id_and_tab_id(user_id, tab_id, db)
    if not tab:
        raise HTTPException(status_code=404, detail="Tab not found")
    return tab


# Create a new tab
@router.post("/users/{user_id}/tabs", response_model=TabResponse)
def create_new_tab(user_id: int, tab_create: TabCreate, db: Session = Depends(get_db)):
    # Ensure user_id in the body matches the path parameter
    if user_id != tab_create.user_id:
        raise HTTPException(
            status_code=400, detail="User ID in path and body must match"
        )
    new_tab = tab_service.create_tab(tab_create, db)
    if not new_tab:
        raise HTTPException(status_code=400, detail="Error creating tab")
    return new_tab


# Delete a tab
@router.delete("/users/{user_id}/tabs/{tab_id}")
def delete_existing_tab(user_id: int, tab_id: int, db: Session = Depends(get_db)):
    success = tab_service.delete_tab(user_id, tab_id, db)
    if not success:
        raise HTTPException(
            status_code=404, detail="Tab not found or error deleting tab"
        )
    return {"detail": "Tab deleted successfully"}


# Update tab name
@router.put("/users/{user_id}/tabs/{tab_id}", response_model=TabResponse)
def update_tab_name(
    user_id: int, tab_id: int, tab_update: TabUpdateName, db: Session = Depends(get_db)
):
    updated_tab = tab_service.update_tab_name(user_id, tab_id, tab_update.tab_name, db)
    if not updated_tab:
        raise HTTPException(status_code=404, detail="Tab not found")
    return updated_tab
