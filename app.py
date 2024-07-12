""" ./app.py"""

from fastapi import FastAPI
from database import engine, Base
from routers import (
    users,
    profiles,
    text_entries,
    audios,
    voice_clones,
    feedbacks,
    guests,
)
import models

# Drop all tables - careful with this
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(guests.router, prefix="/api/v1", tags=["guests"])
app.include_router(profiles.router, prefix="/api/v1", tags=["profiles"])
app.include_router(text_entries.router, prefix="/api/v1", tags=["text_entries"])
app.include_router(audios.router, prefix="/api/v1", tags=["audio"])
app.include_router(voice_clones.router, prefix="/api/v1", tags=["voice_clones"])
app.include_router(feedbacks.router, prefix="/api/v1", tags=["feedback"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
