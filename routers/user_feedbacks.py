""" ./routers/user_feedbacks.py """

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.user_feedback import (
    UserFeedbackCreate,
    UserFeedbackUpdate,
    UserFeedbackResponse,
)
from services import user_feedback_service

router = APIRouter()


@router.post(
    "/feedbacks/",
    response_model=UserFeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_feedback(
    feedback: UserFeedbackCreate, user_id: int, db: Session = Depends(get_db)
):
    result = user_feedback_service.create_feedback(db, feedback, user_id)
    return JSONResponse(content=result, status_code=status.HTTP_201_CREATED)


@router.put("/feedbacks/{feedback_id}", response_model=UserFeedbackResponse)
def update_feedback(
    feedback_id: int,
    feedback: UserFeedbackUpdate,
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_feedback_service.update_feedback(db, feedback_id, feedback, user_id)


@router.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, user_id: int, db: Session = Depends(get_db)):
    deleted_id = user_feedback_service.delete_feedback(db, feedback_id, user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Feedback deleted successfully", "deleted_id": deleted_id},
    )


@router.get("/feedbacks/", response_model=List[UserFeedbackResponse])
def read_feedbacks(
    skip: int = 0, limit: int = 10, user_id: int = None, db: Session = Depends(get_db)
):
    return user_feedback_service.get_feedbacks(db, skip, limit, user_id)


@router.get("/feedbacks/{feedback_id}", response_model=UserFeedbackResponse)
def read_feedback(feedback_id: int, user_id: int, db: Session = Depends(get_db)):
    return user_feedback_service.get_feedback(db, feedback_id, user_id)
