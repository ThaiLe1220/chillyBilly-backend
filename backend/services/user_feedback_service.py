""" ./backend/services/user_feedback_service.py"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import UserFeedback, Audio, User
from schemas.user_feedback import (
    UserFeedbackCreate,
    UserFeedbackUpdate,
    UserFeedbackResponse,
)
from typing import List
from models.audio import AudioStatus  # Import the AudioStatus enum


def create_user_feedback(
    db: Session, user_id: int, feedback: UserFeedbackCreate
) -> UserFeedbackResponse:
    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the audio exists and is ready
    audio = db.query(Audio).filter(Audio.id == feedback.audio_id).first()
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found")

    if audio.status != AudioStatus.READY:
        raise HTTPException(status_code=400, detail="Audio is not ready for feedback")

    # Check if feedback already exists
    existing_feedback = (
        db.query(UserFeedback)
        .filter(
            UserFeedback.user_id == user_id, UserFeedback.audio_id == feedback.audio_id
        )
        .first()
    )
    if existing_feedback:
        raise HTTPException(
            status_code=400, detail="Feedback already exists for this audio"
        )

    # Create new feedback
    db_feedback = UserFeedback(
        user_id=user_id,
        audio_id=feedback.audio_id,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    return UserFeedbackResponse(
        id=db_feedback.id,
        user_id=db_feedback.user_id,
        audio_id=db_feedback.audio_id,
        rating=db_feedback.rating,
        comment=db_feedback.comment,
        created_at=db_feedback.created_at,
        updated_at=db_feedback.updated_at,
    )


def get_user_feedback(db: Session, feedback_id: int) -> UserFeedbackResponse:
    feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return UserFeedbackResponse(
        id=feedback.id,
        user_id=feedback.user_id,
        audio_id=feedback.audio_id,
        rating=feedback.rating,
        comment=feedback.comment,
        created_at=feedback.created_at,
        updated_at=feedback.updated_at,
    )


def get_user_feedbacks(db: Session, user_id: int) -> List[UserFeedbackResponse]:
    feedbacks = db.query(UserFeedback).filter(UserFeedback.user_id == user_id).all()
    return [
        UserFeedbackResponse(
            id=feedback.id,
            user_id=feedback.user_id,
            audio_id=feedback.audio_id,
            rating=feedback.rating,
            comment=feedback.comment,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )
        for feedback in feedbacks
    ]


def update_user_feedback(
    db: Session, feedback_id: int, feedback_update: UserFeedbackUpdate
) -> UserFeedbackResponse:
    db_feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    update_data = feedback_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)

    db.commit()
    db.refresh(db_feedback)
    return UserFeedbackResponse(
        id=db_feedback.id,
        user_id=db_feedback.user_id,
        audio_id=db_feedback.audio_id,
        rating=db_feedback.rating,
        comment=db_feedback.comment,
        created_at=db_feedback.created_at,
        updated_at=db_feedback.updated_at,
    )


def delete_user_feedback(db: Session, feedback_id: int) -> int:
    db_feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(db_feedback)
    db.commit()
    return feedback_id
