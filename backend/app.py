import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import (
    user_feedbacks,
    user_profiles,
    users,
    text_entries,
    audios,
    guests,
    voices,
    tabs,
    tab_generations,
)
import models
import logging
import requests
from requests.exceptions import RequestException


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log environment variables
# Log the current working directory
logger.debug("DATABASE_URL: %s", os.getenv("DATABASE_URL"))
logger.debug("Current working directory: %s", os.getcwd())

TTS_API_URL = os.getenv("TTS_API_URL", "http://localhost:8080")
URL_DELETE_CUSTOM_VOICES = f"{TTS_API_URL}/delete_all_custom_voices"
URL_DELETE_AUDIO = f"{TTS_API_URL}/delete_all_audio"
URL_CREATE_DEFAULT_VOICES = (
    "https://face-swap.12pmtech.link/api/v1/voices/create_defaults/"
)


def resource_request(method, url):
    try:
        response = requests.request(method, url, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logger.info("Successfully executed %s request to %s", method.upper(), url)
        return response.json()  # Return JSON response
    except RequestException as e:
        logger.error(
            "Failed to execute %s request to %s: %s", method.upper(), url, str(e)
        )
        return None


# Drop all tables - careful with this
# Base.metadata.drop_all(bind=engine)
# resource_request("DELETE", URL_DELETE_CUSTOM_VOICES)
# resource_request("DELETE", URL_DELETE_AUDIO)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="/app/output"), name="static")


app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(guests.router, prefix="/api/v1", tags=["guests"])
app.include_router(user_profiles.router, prefix="/api/v1", tags=["user_profiles"])
app.include_router(text_entries.router, prefix="/api/v1", tags=["text_entries"])
app.include_router(audios.router, prefix="/api/v1", tags=["audios"])
app.include_router(voices.router, prefix="/api/v1", tags=["voices"])
app.include_router(user_feedbacks.router, prefix="/api/v1", tags=["user_feedbacks"])
app.include_router(tabs.router, prefix="/api/v1", tags=["tabs"])
app.include_router(tab_generations.router, prefix="/api/v1", tags=["tab_generations"])


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
