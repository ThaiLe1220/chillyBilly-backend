""" ./backend/services/tab_service.py"""

from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Tab
from models.user import User
from models.guest import Guest
from schemas.tab import TabResponse, TabCreate

def get_tabs_by_user_id(user_id: int, db: Session) -> List[TabResponse]:
    return db.query(Tab).filter(Tab.user_id == user_id).order_by(Tab.id.desc()).all()

def get_tab_by_user_id_and_tab_id(user_id: int, tab_id: int, db: Session) -> TabResponse:
    return db.query(Tab).filter(Tab.user_id == user_id, Tab.id == tab_id).first()

def create_tab(tab_create: TabCreate, db: Session) -> TabResponse:
    if tab_create.user_id is None and tab_create.guest_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either user_id or guest_id must be provided",
        )

    if tab_create.user_id is not None and tab_create.guest_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only one of user_id or guest_id should be provided",
        )

    # Check if user exists
    if tab_create.user_id is not None:
        user = db.query(User).filter(User.id == tab_create.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {tab_create.user_id} not found",
            )

    # Check if guest exists
    if tab_create.guest_id is not None:
        guest = db.query(Guest).filter(Guest.id == tab_create.guest_id).first()
        if not guest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Guest with id {tab_create.guest_id} not found",
            )
    
    try:
        # Create a new Tab instance
        new_tab = Tab(**tab_create.dict(exclude_unset=True))
        
        # Add and commit the new tab to the database
        db.add(new_tab)
        db.commit()
        db.refresh(new_tab)
        
        # Return the tab as TabResponse
        return TabResponse(
            id=new_tab.id,
            tab_name=new_tab.tab_name
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the new tab",
        ) from e

def delete_tab(user_id: int, tab_id: int, db: Session) -> bool:
    tab = db.query(Tab).filter(Tab.user_id == user_id, Tab.id == tab_id).first()
    if tab:
        db.delete(tab)
        db.commit()
        return True
    return False