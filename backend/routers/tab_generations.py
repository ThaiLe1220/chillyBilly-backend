""" ./backend/routers/tab_generations.py"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from schemas.tab_generation import TabGenerationCreate, TabGenerationResponse
from services.tab_generation_service import create_tab_generation, get_all_tab_generations_of_a_tab, get_all_tab_generations_of_user, get_tab_generation, get_tab_generation_1st, verify_user_exists, verify_tab_exists
from database import get_db
from models import User, Tab

router = APIRouter()

@router.post("/users/{user_id}/tabs/{tab_id}/tab_generations/", response_model=TabGenerationResponse)
def create_new_tab_generation(
    user_id: int,
    tab_id: int,
    tab_generation_create: TabGenerationCreate,
    db: Session = Depends(get_db)
):
    try:
        # Create tab generation and handle possible exceptions
        return create_tab_generation(user_id, tab_id, tab_generation_create, db)
    except Exception as e:
        # Return detailed error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the tab generation: {str(e)}",
        ) from e
    
@router.get("/users/{user_id}/tab_generations/", response_model=List[TabGenerationResponse])
def read_all_tab_generations_of_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        if not verify_user_exists(user_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        tab_generations = get_all_tab_generations_of_user(user_id, db)

        return tab_generations
    except HTTPException as e:
        # Re-raise HTTPExceptions to avoid double-wrapping
        raise e
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tab generations: {str(e)}"
        ) from e
        
@router.get("/users/{user_id}/tabs/{tab_id}/tab_generations/", response_model=List[TabGenerationResponse])
def read_all_tab_generations_of_a_tab(
    user_id: int,
    tab_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Validate user existence
        if not verify_user_exists(user_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Validate tab existence
        if not verify_tab_exists(tab_id, db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tab not found"
            )

        # Fetch all tab generations for the given user and tab
        tab_generations = get_all_tab_generations_of_a_tab(user_id, tab_id, db)
        
        return tab_generations
    except HTTPException as e:
        # Re-raise HTTPExceptions to avoid double-wrapping
        raise e
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tab generations: {str(e)}"
        ) from e
        
        
@router.get("/users/{user_id}/tabs/{tab_id}/tab_generations/1st", response_model=TabGenerationResponse)
def read_tab_generation_1st(
    user_id: int,
    tab_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Get tab generation and handle possible exceptions
        tab_generation = get_tab_generation_1st(user_id, tab_id, db)
        if tab_generation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TabGeneration not found"
            )
        return tab_generation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the tab generation",
        ) from e


@router.get("/users/{user_id}/tabs/{tab_id}/tab_generations/{tab_generation_id}", response_model=Optional[TabGenerationResponse])
def read_tab_generation(
    user_id: int,
    tab_id: int,
    tab_generation_id: int,
    db: Session = Depends(get_db)
):
    try:
        # Get tab generation and handle possible exceptions
        tab_generation = get_tab_generation(tab_generation_id, user_id, tab_id, db)
        if tab_generation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TabGeneration not found"
            )
        return tab_generation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving tab generation: {str(e)}"
        ) from e