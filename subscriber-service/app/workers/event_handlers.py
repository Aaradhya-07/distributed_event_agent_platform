from celery import Celery
from shared.config import Settings
from shared.models import UserInteractionEvent, ChemicalResearchEvent, UserInteractionEventDB, ChemicalResearchEventDB
from app.infrastructure.db import AsyncSessionLocal
from app.infrastructure.llm_client import GroqLLMClient
import json
from sqlalchemy.future import select
from datetime import datetime

settings = Settings()

def make_celery_app(settings: Settings):
    """Create and configure a Celery app instance with the given settings."""
    return Celery(
        'subscriber',
        broker=settings.celery_broker_url,
    )

celery_app = make_celery_app(settings)

@celery_app.task
def process_user_event(event_data):
    """Celery task to process and store a user interaction event in the database.
    Args:
        event_data: JSON string of the user interaction event.
    """
    event = UserInteractionEvent.parse_raw(event_data)
    async def db_task():
        async with AsyncSessionLocal() as session:
            db_event = UserInteractionEventDB(
                user_id=event.user_id,
                event_type=event.event_type,
                timestamp=datetime.fromisoformat(event.timestamp),
                event_metadata=event.event_metadata
            )
            session.add(db_event)
            await session.commit()
    import asyncio; asyncio.run(db_task())

@celery_app.task
def process_chemical_event(event_data):
    """Celery task to process a chemical research event, enrich with LLM, and store in the database.
    Args:
        event_data: JSON string of the chemical research event.
    """
    event = ChemicalResearchEvent.parse_raw(event_data)
    async def db_task():
        async with AsyncSessionLocal() as session:
            llm_client = GroqLLMClient(settings)
            try:
                enriched = await llm_client.extract_properties(event.data)
                event_data_enriched = {**event.data, **enriched}
            except Exception as e:
                event_data_enriched = {**event.data, "llm_error": str(e)}
            db_event = ChemicalResearchEventDB(
                molecule_id=event.molecule_id,
                researcher=event.researcher,
                data=event_data_enriched,
                timestamp=datetime.fromisoformat(event.timestamp)
            )
            session.add(db_event)
            await session.commit()
    import asyncio; asyncio.run(db_task()) 