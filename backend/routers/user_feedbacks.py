""" ./backend/routers/user_feedback.py"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.user_feedback import (
    UserFeedbackCreate,
    UserFeedbackUpdate,
    UserFeedbackResponse,
)
from services import user_feedback_service

router = APIRouter()


@router.post("/users/{user_id}/feedback", response_model=UserFeedbackResponse)
def create_user_feedback(
    user_id: int, feedback: UserFeedbackCreate, db: Session = Depends(get_db)
):
    return user_feedback_service.create_user_feedback(db, user_id, feedback)


@router.get("/feedback/{feedback_id}", response_model=UserFeedbackResponse)
def get_user_feedback(feedback_id: int, db: Session = Depends(get_db)):
    return user_feedback_service.get_user_feedback(db, feedback_id)


@router.get("/users/{user_id}/feedback", response_model=List[UserFeedbackResponse])
def get_user_feedbacks(user_id: int, db: Session = Depends(get_db)):
    return user_feedback_service.get_user_feedbacks(db, user_id)


@router.put("/feedback/{feedback_id}", response_model=UserFeedbackResponse)
def update_user_feedback(
    feedback_id: int, feedback_update: UserFeedbackUpdate, db: Session = Depends(get_db)
):
    return user_feedback_service.update_user_feedback(db, feedback_id, feedback_update)


@router.delete("/feedback/{feedback_id}")
def delete_user_feedback(feedback_id: int, db: Session = Depends(get_db)):
    deleted_id = user_feedback_service.delete_user_feedback(db, feedback_id)
    return {"message": "Feedback deleted successfully", "deleted_id": deleted_id}
