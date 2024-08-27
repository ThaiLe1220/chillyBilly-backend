from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models.tab_generation import TabGeneration
from fastapi import BackgroundTasks
from models.text_entry import TextEntry
from models.audio import Audio
from models import User, Tab
from schemas.tab_generation import TabGenerationCreate, TabGenerationResponse
from schemas.text_entry import TextEntryCreate
from schemas.audio import AudioCreate, AudioResponse
from services import text_entry_service, audio_service
from datetime import datetime
from typing import Optional, List


def verify_user_exists(user_id: int, db: Session) -> bool:
    return db.query(User).filter(User.id == user_id).first() is not None


def verify_tab_exists(tab_id: int, db: Session) -> bool:
    return db.query(Tab).filter(Tab.id == tab_id).first() is not None


async def create_tab_generation(
    user_id: int,
    tab_id: int,
    tab_generation_create: TabGenerationCreate,
    db: Session,
    background_tasks: BackgroundTasks,
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
            created_at=tab_generation_create.created_at or datetime.utcnow(),
        )

        db.add(tab_generation)
        db.commit()
        db.refresh(tab_generation)

        text_entry_created = None
        audio_created = None

        # Create TextEntry if provided
        if tab_generation_create.text_entry_content:
            text_entry_create = TextEntryCreate(
                content=tab_generation_create.text_entry_content,
                language=tab_generation_create.language,
                tab_generation_id=tab_generation.id,
                user_id=user_id,
            )
            text_entry_created = text_entry_service.create_text_entry(
                db, text_entry_create
            )

        if text_entry_created:
            audio_create = AudioCreate(
                text_entry_id=text_entry_created.id,
                voice_id=tab_generation_create.voice_id,
                tab_generation_id=tab_generation.id,
            )
            audio_created = await audio_service.create_audio(
                db=db, audio=audio_create, background_tasks=background_tasks
            )

        return TabGenerationResponse(
            id=tab_generation.id,
            tab_id=tab_generation.tab_id,
            created_at=tab_generation.created_at,
            text_entry_content=tab_generation_create.text_entry_content,
            audio=audio_created,
        )
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating tab generation: {str(e)}")


def get_all_tab_generations_of_user(
    user_id: int, db: Session
) -> List[TabGenerationResponse]:
    try:
        tab_generations = (
            db.query(TabGeneration)
            .join(Tab, TabGeneration.tab_id == Tab.id)
            .filter(Tab.user_id == user_id)
            .outerjoin(TextEntry, TextEntry.tab_generation_id == TabGeneration.id)
            .outerjoin(Audio, Audio.tab_generation_id == TabGeneration.id)
            .all()
        )

        # Return the list of TabGenerationResponse objects with concatenated TextEntry content
        return [
            TabGenerationResponse(
                id=tab_generation.id,
                tab_id=tab_generation.tab_id,
                created_at=tab_generation.created_at,
                text_entry_content=(
                    " ".join(entry.content for entry in tab_generation.text_entry)
                    if tab_generation.text_entry
                    else None
                ),
                audio=(
                    AudioResponse(
                        id=tab_generation.audio[0].id,
                        text_entry_id=tab_generation.audio[0].text_entry_id,
                        voice_id=tab_generation.audio[0].voice_id,
                        audio_duration=tab_generation.audio[0].audio_duration,
                        audio_name=tab_generation.audio[0].audio_name,
                        audio_path=tab_generation.audio[0].audio_path,
                        audio_size=tab_generation.audio[0].audio_size,
                        audio_wavelength=tab_generation.audio[0].audio_wavelength,
                        delete_url=tab_generation.audio[0].delete_url,
                        download_url=tab_generation.audio[0].download_url,
                        generation_time=tab_generation.audio[0].generation_time,
                        language=tab_generation.audio[0].language,
                        message=tab_generation.audio[0].message,
                        mime_type=tab_generation.audio[0].mime_type,
                        preset=tab_generation.audio[0].preset,
                        sample_rate=tab_generation.audio[0].sample_rate,
                        text_length=tab_generation.audio[0].text_length,
                        timestamp=tab_generation.audio[0].timestamp,
                        voice_name=tab_generation.audio[0].voice_name,
                        status=tab_generation.audio[0].status,
                        created_at=tab_generation.audio[0].created_at,
                        updated_at=tab_generation.audio[0].updated_at,
                    )
                    if tab_generation.audio
                    else None
                ),
            )
            for tab_generation in tab_generations
        ]
    except Exception as e:
        raise Exception(f"An error occurred while retrieving tab generations: {e}")


def get_all_tab_generations_of_a_tab(
    user_id: int, tab_id: int, db: Session
) -> List[TabGenerationResponse]:
    try:
        # Query tab generations filtered by user_id and tab_id, explicitly joining with TextEntry
        tab_generations = (
            db.query(TabGeneration)
            .join(Tab, TabGeneration.tab_id == Tab.id)
            .filter(Tab.user_id == user_id)
            .filter(TabGeneration.tab_id == tab_id)
            .outerjoin(TextEntry, TextEntry.tab_generation_id == TabGeneration.id)
            .outerjoin(Audio, Audio.tab_generation_id == TabGeneration.id)
            .all()
        )

        # Return the list of TabGenerationResponse objects with concatenated TextEntry content
        return [
            TabGenerationResponse(
                id=tab_generation.id,
                tab_id=tab_generation.tab_id,
                created_at=tab_generation.created_at,
                text_entry_content=(
                    " ".join(entry.content for entry in tab_generation.text_entry)
                    if tab_generation.text_entry
                    else None
                ),
                audio=(
                    AudioResponse(
                        id=tab_generation.audio[0].id,
                        text_entry_id=tab_generation.audio[0].text_entry_id,
                        voice_id=tab_generation.audio[0].voice_id,
                        audio_duration=tab_generation.audio[0].audio_duration,
                        audio_name=tab_generation.audio[0].audio_name,
                        audio_path=tab_generation.audio[0].audio_path,
                        audio_size=tab_generation.audio[0].audio_size,
                        audio_wavelength=tab_generation.audio[0].audio_wavelength,
                        delete_url=tab_generation.audio[0].delete_url,
                        download_url=tab_generation.audio[0].download_url,
                        generation_time=tab_generation.audio[0].generation_time,
                        language=tab_generation.audio[0].language,
                        message=tab_generation.audio[0].message,
                        mime_type=tab_generation.audio[0].mime_type,
                        preset=tab_generation.audio[0].preset,
                        sample_rate=tab_generation.audio[0].sample_rate,
                        text_length=tab_generation.audio[0].text_length,
                        timestamp=tab_generation.audio[0].timestamp,
                        voice_name=tab_generation.audio[0].voice_name,
                        status=tab_generation.audio[0].status,
                        created_at=tab_generation.audio[0].created_at,
                        updated_at=tab_generation.audio[0].updated_at,
                    )
                    if tab_generation.audio
                    else None
                ),
            )
            for tab_generation in tab_generations
        ]
    except Exception as e:
        raise Exception(f"An error occurred while retrieving tab generations: {e}")


def get_tab_generation(
    tab_generation_id: int, user_id: int, tab_id: int, db: Session
) -> Optional[TabGenerationResponse]:

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
            .outerjoin(Audio, Audio.tab_generation_id == TabGeneration.id)
            .filter(TabGeneration.id == tab_generation_id)
            .first()
        )

        if not result:
            return None

        print(f"Debug: TabGeneration ID: {result.id}")
        print(f"Debug: Audio: {result.audio}")
        if result.audio:
            print(f"Debug: Audio ID: {result.audio.id}")
            print(f"Debug: Audio text_entry_id: {result.audio.text_entry_id}")
            print(f"Debug: Audio status: {result.audio.status}")

        return TabGenerationResponse(
            id=result.id,
            tab_id=result.tab_id,
            created_at=result.created_at,
            text_entry_content=(
                " ".join(entry.content for entry in result.text_entry)
                if result.text_entry
                else None
            ),
            audio=(
                AudioResponse(
                    id=result.audio[0].id,
                    text_entry_id=result.audio[0].text_entry_id,
                    voice_id=result.audio[0].voice_id,
                    audio_duration=result.audio[0].audio_duration,
                    audio_name=result.audio[0].audio_name,
                    audio_path=result.audio[0].audio_path,
                    audio_size=result.audio[0].audio_size,
                    audio_wavelength=result.audio[0].audio_wavelength,
                    delete_url=result.audio[0].delete_url,
                    download_url=result.audio[0].download_url,
                    generation_time=result.audio[0].generation_time,
                    language=result.audio[0].language,
                    message=result.audio[0].message,
                    mime_type=result.audio[0].mime_type,
                    preset=result.audio[0].preset,
                    sample_rate=result.audio[0].sample_rate,
                    text_length=result.audio[0].text_length,
                    timestamp=result.audio[0].timestamp,
                    voice_name=result.audio[0].voice_name,
                    status=result.audio[0].status,
                    created_at=result.audio[0].created_at,
                    updated_at=result.audio[0].updated_at,
                )
                if result.audio
                else None
            ),
        )
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the tab generation: {e}")


def get_tab_generation_1st(
    user_id: int, tab_id: int, db: Session
) -> Optional[TabGenerationResponse]:
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
            .outerjoin(Audio, Audio.tab_generation_id == TabGeneration.id)
            .order_by(TabGeneration.created_at.desc())
            .first()
        )

        if not result:
            return None

        print(f"Debug: TabGeneration ID: {result.id}")
        print(f"Debug: Audio: {result.audio}")
        if result.audio:
            print(f"Debug: Audio ID: {result.audio.id}")
            print(f"Debug: Audio text_entry_id: {result.audio.text_entry_id}")
            print(f"Debug: Audio status: {result.audio.status}")

        return TabGenerationResponse(
            id=result.id,
            tab_id=result.tab_id,
            created_at=result.created_at,
            text_entry_content=(
                " ".join(entry.content for entry in result.text_entry)
                if result.text_entry
                else None
            ),
            audio=(
                AudioResponse(
                    id=result.audio[0].id,
                    text_entry_id=result.audio[0].text_entry_id,
                    voice_id=result.audio[0].voice_id,
                    audio_duration=result.audio[0].audio_duration,
                    audio_name=result.audio[0].audio_name,
                    audio_path=result.audio[0].audio_path,
                    audio_size=result.audio[0].audio_size,
                    audio_wavelength=result.audio[0].audio_wavelength,
                    delete_url=result.audio[0].delete_url,
                    download_url=result.audio[0].download_url,
                    generation_time=result.audio[0].generation_time,
                    language=result.audio[0].language,
                    message=result.audio[0].message,
                    mime_type=result.audio[0].mime_type,
                    preset=result.audio[0].preset,
                    sample_rate=result.audio[0].sample_rate,
                    text_length=result.audio[0].text_length,
                    timestamp=result.audio[0].timestamp,
                    voice_name=result.audio[0].voice_name,
                    status=result.audio[0].status,
                    created_at=result.audio[0].created_at,
                    updated_at=result.audio[0].updated_at,
                )
                if result.audio
                else None
            ),
        )
    except Exception as e:
        raise Exception(
            f"An error occurred while retrieving the latest tab generation: {e}"
        )
