from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    Boolean,
    Text,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    two_factor_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    last_active_date = Column(DateTime)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime)
    preferred_language = Column(Enum("vi", "en", name="language_enum"))

    user = relationship("User", back_populates="profile")


User.profile = relationship("UserProfile", uselist=False, back_populates="user")


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    expiry_time = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class TextEntry(Base):
    __tablename__ = "text_entries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    language = Column(Enum("vi", "en", name="language_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="text_entries")


User.text_entries = relationship(
    "TextEntry", order_by=TextEntry.id, back_populates="user"
)


class GeneratedAudio(Base):
    __tablename__ = "generated_audio"
    id = Column(Integer, primary_key=True)
    text_id = Column(Integer, ForeignKey("text_entries.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String, nullable=False)
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    text_entry = relationship("TextEntry")
    user = relationship("User")


class VoiceClone(Base):
    __tablename__ = "voice_clones"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_file_path = Column(String, nullable=False)
    processed_file_path = Column(String)
    status = Column(
        Enum("processing", "ready", "failed", name="clone_status_enum"), nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class UsageHistory(Base):
    __tablename__ = "usage_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action_type = Column(
        Enum("text_entry", "audio_generation", "voice_upload", name="action_type_enum"),
        nullable=False,
    )
    related_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class ErrorLog(Base):
    __tablename__ = "error_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_type = Column(String, nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text)


class APIUsage(Base):
    __tablename__ = "api_usage"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String, nullable=False)
    request_count = Column(Integer, default=0)
    last_request = Column(DateTime, default=datetime.utcnow)
    daily_limit = Column(Integer)

    user = relationship("User")


class UserFeedback(Base):
    __tablename__ = "user_feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    audio_id = Column(Integer, ForeignKey("generated_audio.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    audio = relationship("GeneratedAudio")


class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True)
    setting_key = Column(String, unique=True, nullable=False)
    setting_value = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)


engine = create_engine("postgresql://tts_user:tts_eugene@localhost/tts_app")
Base.metadata.create_all(engine)
