from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
from models import (
    engine,
    User,
    UserProfile,
    Session as DbSession,
    TextEntry,
    GeneratedAudio,
    VoiceClone,
    UsageHistory,
    ErrorLog,
    APIUsage,
    UserFeedback,
    SystemSetting,
)

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime
    preferred_language: str


class UserProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime
    preferred_language: str


class UserProfileUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[datetime]
    preferred_language: Optional[str]


class TextEntryCreate(BaseModel):
    content: str
    language: str


class TextEntryResponse(BaseModel):
    id: int
    content: str
    language: str
    created_at: datetime


class GeneratedAudioCreate(BaseModel):
    text_id: int
    file_path: str
    duration: float


class GeneratedAudioResponse(BaseModel):
    id: int
    text_id: int
    file_path: str
    duration: float
    created_at: datetime


class VoiceCloneCreate(BaseModel):
    original_file_path: str


class VoiceCloneResponse(BaseModel):
    id: int
    original_file_path: str
    processed_file_path: Optional[str]
    status: str
    created_at: datetime


class UserFeedbackCreate(BaseModel):
    audio_id: int
    rating: int
    comment: Optional[str]


class UserFeedbackResponse(BaseModel):
    id: int
    audio_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime


# API endpoints
"""
User management (create, read, update, delete)
User profile management (create, update)
Text entries management (create, read, delete)
Generated audio creation and retrieval
Voice clone management (create, read, delete)
User feedback management (create, read)
System settings management (create, read, update)
API usage logging and retrieval
Error logging and retrieval
Session management (create, read, delete)
Usage history logging and retrieval
"""


@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username, email=user.email, password_hash=user.password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            raise HTTPException(status_code=400, detail="Username already exists")
        elif "email" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="An integrity error occurred")
    return db_user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.password_hash = (
            user_update.password
        )  # In production, hash this password

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}


@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.post("/users/{user_id}/profile/", response_model=UserProfileResponse)
def create_user_profile(
    user_id: int, profile: UserProfileCreate, db: Session = Depends(get_db)
):
    db_profile = UserProfile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.put("/users/{user_id}/profile/", response_model=UserProfileResponse)
def update_user_profile(
    user_id: int, profile_update: UserProfileUpdate, db: Session = Depends(get_db)
):
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile


@app.delete(
    "/users/{user_id}/text_entries/{text_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_text_entry(user_id: int, text_id: int, db: Session = Depends(get_db)):
    db_text_entry = (
        db.query(TextEntry)
        .filter(TextEntry.id == text_id, TextEntry.user_id == user_id)
        .first()
    )
    if not db_text_entry:
        raise HTTPException(status_code=404, detail="Text entry not found")
    db.delete(db_text_entry)
    db.commit()
    return {"ok": True}


@app.post("/users/{user_id}/text_entries/", response_model=TextEntryResponse)
def create_text_entry(
    user_id: int, text_entry: TextEntryCreate, db: Session = Depends(get_db)
):
    db_text_entry = TextEntry(**text_entry.dict(), user_id=user_id)
    db.add(db_text_entry)
    db.commit()
    db.refresh(db_text_entry)
    return db_text_entry


@app.get("/users/{user_id}/text_entries/", response_model=List[TextEntryResponse])
def read_user_text_entries(user_id: int, db: Session = Depends(get_db)):
    text_entries = db.query(TextEntry).filter(TextEntry.user_id == user_id).all()
    return text_entries


@app.post("/generated_audio/", response_model=GeneratedAudioResponse)
def create_generated_audio(audio: GeneratedAudioCreate, db: Session = Depends(get_db)):
    db_audio = GeneratedAudio(**audio.dict())
    db.add(db_audio)
    db.commit()
    db.refresh(db_audio)
    return db_audio


@app.get("/generated_audio/{audio_id}", response_model=GeneratedAudioResponse)
def get_generated_audio(audio_id: int, db: Session = Depends(get_db)):
    db_audio = db.query(GeneratedAudio).filter(GeneratedAudio.id == audio_id).first()
    if not db_audio:
        raise HTTPException(status_code=404, detail="Generated audio not found")
    return db_audio


@app.post("/users/{user_id}/voice_clones/", response_model=VoiceCloneResponse)
def create_voice_clone(
    user_id: int, voice_clone: VoiceCloneCreate, db: Session = Depends(get_db)
):
    db_voice_clone = VoiceClone(
        **voice_clone.dict(), user_id=user_id, status="processing"
    )
    db.add(db_voice_clone)
    db.commit()
    db.refresh(db_voice_clone)
    return db_voice_clone


@app.get("/users/{user_id}/voice_clones/", response_model=List[VoiceCloneResponse])
def get_user_voice_clones(user_id: int, db: Session = Depends(get_db)):
    voice_clones = db.query(VoiceClone).filter(VoiceClone.user_id == user_id).all()
    return voice_clones


@app.delete(
    "/users/{user_id}/voice_clones/{clone_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_voice_clone(user_id: int, clone_id: int, db: Session = Depends(get_db)):
    db_voice_clone = (
        db.query(VoiceClone)
        .filter(VoiceClone.id == clone_id, VoiceClone.user_id == user_id)
        .first()
    )
    if not db_voice_clone:
        raise HTTPException(status_code=404, detail="Voice clone not found")
    db.delete(db_voice_clone)
    db.commit()
    return {"ok": True}


@app.post("/users/{user_id}/feedback/", response_model=UserFeedbackResponse)
def create_user_feedback(
    user_id: int, feedback: UserFeedbackCreate, db: Session = Depends(get_db)
):
    db_feedback = UserFeedback(**feedback.dict(), user_id=user_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@app.get("/users/{user_id}/feedback/", response_model=List[UserFeedbackResponse])
def get_user_feedback(user_id: int, db: Session = Depends(get_db)):
    feedback = db.query(UserFeedback).filter(UserFeedback.user_id == user_id).all()
    return feedback


@app.get("/system_settings/{setting_key}")
def get_system_setting(setting_key: str, db: Session = Depends(get_db)):
    setting = (
        db.query(SystemSetting).filter(SystemSetting.setting_key == setting_key).first()
    )
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return {"key": setting.setting_key, "value": setting.setting_value}


@app.post("/system_settings/")
def create_system_setting(key: str, value: str, db: Session = Depends(get_db)):
    db_setting = SystemSetting(setting_key=key, setting_value=value)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return {"key": db_setting.setting_key, "value": db_setting.setting_value}


@app.put("/system_settings/{setting_key}")
def update_system_setting(setting_key: str, value: str, db: Session = Depends(get_db)):
    setting = (
        db.query(SystemSetting).filter(SystemSetting.setting_key == setting_key).first()
    )
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting.setting_value = value
    db.commit()
    db.refresh(setting)
    return {"key": setting.setting_key, "value": setting.setting_value}


# New endpoints for API usage, error logs, sessions, and usage history
@app.post("/api_usage/")
def log_api_usage(user_id: int, endpoint: str, db: Session = Depends(get_db)):
    usage = APIUsage(user_id=user_id, endpoint=endpoint)
    db.add(usage)
    db.commit()
    return {"message": "API usage logged"}


@app.get("/api_usage/{user_id}")
def get_api_usage(user_id: int, db: Session = Depends(get_db)):
    usage = db.query(APIUsage).filter(APIUsage.user_id == user_id).all()
    return usage


@app.post("/error_logs/")
def log_error(
    error_type: str,
    error_message: str,
    stack_trace: str = None,
    db: Session = Depends(get_db),
):
    error_log = ErrorLog(
        error_type=error_type, error_message=error_message, stack_trace=stack_trace
    )
    db.add(error_log)
    db.commit()
    return {"message": "Error logged"}


@app.get("/error_logs/")
def get_error_logs(db: Session = Depends(get_db)):
    logs = db.query(ErrorLog).all()
    return logs


@app.post("/sessions/")
def create_session(user_id: int, db: Session = Depends(get_db)):
    token = secrets.token_urlsafe()
    expiry_time = datetime.utcnow() + timedelta(
        hours=24
    )  # Set session to expire in 24 hours
    session = DbSession(user_id=user_id, token=token, expiry_time=expiry_time)
    db.add(session)
    db.commit()
    return {"token": token}


@app.get("/sessions/{token}")
def get_session(token: str, db: Session = Depends(get_db)):
    session = db.query(DbSession).filter(DbSession.token == token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.delete("/sessions/{token}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(token: str, db: Session = Depends(get_db)):
    session = db.query(DbSession).filter(DbSession.token == token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"ok": True}


@app.post("/usage_history/")
def log_usage(
    user_id: int, action_type: str, related_id: int, db: Session = Depends(get_db)
):
    usage = UsageHistory(
        user_id=user_id, action_type=action_type, related_id=related_id
    )
    db.add(usage)
    db.commit()
    return {"message": "Usage logged"}


@app.get("/usage_history/{user_id}")
def get_usage_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(UsageHistory).filter(UsageHistory.user_id == user_id).all()
    return history


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
