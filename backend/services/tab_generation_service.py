from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.tab_generation import TabGeneration
from models.text_entry import TextEntry
from models import User, Tab
from schemas.tab_generation import TabGenerationCreate, TabGenerationResponse
from schemas.text_entry import TextEntryCreate
from services import text_entry_service
from datetime import datetime
from typing import Optional, List

def verify_user_exists(user_id: int, db: Session) -> bool:
    return db.query(User).filter(User.id == user_id).first() is not None

def verify_tab_exists(tab_id: int, db: Session) -> bool:
    return db.query(Tab).filter(Tab.id == tab_id).first() is not None

def create_tab_generation(
    user_id: int,
    tab_id: int,
    tab_generation_create: TabGenerationCreate,
    db: Session
) -> TabGenerationResponse:
    # Verify that the user and tab exist
    if not verify_user_exists(user_id, db):
        raise ValueError("User not found")
    
    if not verify_tab_exists(tab_id, db):
        raise ValueError("Tab not found")

    try:
        # Create TabGeneration first
        tab_generation = TabGeneration(
            tab_id=tab_generation_create.tab_id,
            created_at=tab_generation_create.created_at or datetime.utcnow()
        )
        
        db.add(tab_generation)
        db.commit()
        db.refresh(tab_generation)
        
        # Create TextEntry if provided
        if tab_generation_create.text_entry_content:
            text_entry_create = TextEntryCreate(
                content=tab_generation_create.text_entry_content,
                language=tab_generation_create.language,  # Default language or derived from request if needed
                tab_generation_id=tab_generation.id,
                user_id=user_id
            )
            text_entry_service.create_text_entry(db, text_entry_create)
        
        return TabGenerationResponse(
            id=tab_generation.id,
            tab_id=tab_generation.tab_id,
            created_at=tab_generation.created_at,
            text_entry_content=tab_generation_create.text_entry_content
        )
    except Exception as e:
        if isinstance(db, Session):
            db.rollback()
        raise Exception(f"Error creating tab generation: {str(e)}")
    
def get_all_tab_generations(user_id: int, tab_id: int, db: Session) -> List[TabGenerationResponse]:
    try:
        # Query tab generations filtered by user_id and tab_id, explicitly joining with TextEntry
        tab_generations = (
            db.query(TabGeneration)
            .join(Tab, TabGeneration.tab_id == Tab.id)
            .filter(Tab.user_id == user_id)
            .filter(TabGeneration.tab_id == tab_id)
            .outerjoin(TextEntry, TextEntry.tab_generation_id == TabGeneration.id)
            .all()
        )
        
        # Return the list of TabGenerationResponse objects with concatenated TextEntry content
        return [
            TabGenerationResponse(
                id=tab_generation.id,
                tab_id=tab_generation.tab_id,
                created_at=tab_generation.created_at,
                text_entry_content=" ".join(entry.content for entry in tab_generation.text_entry) if tab_generation.text_entry else None
            )
            for tab_generation in tab_generations
        ]
    except Exception as e:
        raise Exception(f"An error occurred while retrieving tab generations: {e}")
    

def get_tab_generation(tab_generation_id: int, user_id: int, tab_id: int, db: Session) -> Optional[TabGenerationResponse]:
    # Verify that the user and tab exist
    if not verify_user_exists(user_id, db):
        raise ValueError("User not found")
    
    if not verify_tab_exists(tab_id, db):
        raise ValueError("Tab not found")
    
    try:
        tab_generation = db.query(TabGeneration).filter(TabGeneration.id == tab_generation_id).first()
        if not tab_generation:
            return None

        text_entry_content = None
        if tab_generation.text_entry_id:
            text_entry = db.query(TextEntry).filter(TextEntry.id == tab_generation.text_entry_id).first()
            if text_entry:
                text_entry_content = text_entry.content
        
        return TabGenerationResponse(
            id=tab_generation.id,
            tab_id=tab_generation.tab_id,
            created_at=tab_generation.created_at,
            text_entry_content=text_entry_content
        )
    except NoResultFound:
        return None
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the tab generation: {e}")
    
def get_tab_generation_1st(user_id: int, tab_id: int, db: Session) -> Optional[TabGenerationResponse]:
    
        # Verify that the user and tab exist
    if not verify_user_exists(user_id, db):
        raise ValueError("User not found")
    
    if not verify_tab_exists(tab_id, db):
        raise ValueError("Tab not found")
    
    try:
        # Query for all tab generations filtered by user_id and tab_id, joining with TextEntry
        result = (
            db.query(TabGeneration)
            .join(Tab, TabGeneration.tab_id == Tab.id)
            .filter(Tab.user_id == user_id)
            .filter(TabGeneration.tab_id == tab_id)
            .outerjoin(TextEntry, TextEntry.tab_generation_id == TabGeneration.id)
            .order_by(TabGeneration.created_at.desc())
            .first()
        )
        
        if not result:
            return None

        return TabGenerationResponse(
                id=result.id,
                tab_id=result.tab_id,
                created_at=result.created_at,
                text_entry_content=" ".join(entry.content for entry in result.text_entry) if result.text_entry else None
            )    
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the latest tab generation: {e}")