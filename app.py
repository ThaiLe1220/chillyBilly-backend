""" ./app.py"""

from fastapi import FastAPI
from database import engine, Base
from routers import (
    user_feedbacks,
    user_profiles,
    users,
    text_entries,
    audios,
    guests,
    voices,
)
import models

# Drop all tables - careful with this
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(guests.router, prefix="/api/v1", tags=["guests"])
app.include_router(user_profiles.router, prefix="/api/v1", tags=["user_profiles"])
app.include_router(text_entries.router, prefix="/api/v1", tags=["text_entries"])
app.include_router(audios.router, prefix="/api/v1", tags=["audios"])
app.include_router(voices.router, prefix="/api/v1", tags=["voices"])
# app.include_router(user_feedbacks.router, prefix="/api/v1", tags=["user_feedbacks"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
