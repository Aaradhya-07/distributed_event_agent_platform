from celery import Celery
from shared.config import Settings
from shared.models import UserInteractionEvent, ChemicalResearchEvent, UserInteractionEventDB, ChemicalResearchEventDB
from app.infrastructure.db import AsyncSessionLocal
import json
from sqlalchemy.future import select
from datetime import datetime

settings = Settings()
celery_app = Celery(
    'subscriber',
    broker='redis://localhost:6379/0',  # You can update this if using a different broker
)

@celery_app.task
def process_user_event(event_data):
    event = UserInteractionEvent.parse_raw(event_data)
    async def db_task():
        async with AsyncSessionLocal() as session:
            db_event = UserInteractionEventDB(
                user_id=event.user_id,
                event_type=event.event_type,
                timestamp=datetime.fromisoformat(event.timestamp),
                metadata=event.metadata
            )
            session.add(db_event)
            await session.commit()
    import asyncio; asyncio.run(db_task())

@celery_app.task
def process_chemical_event(event_data):
    event = ChemicalResearchEvent.parse_raw(event_data)
    async def db_task():
        async with AsyncSessionLocal() as session:
            db_event = ChemicalResearchEventDB(
                molecule_id=event.molecule_id,
                researcher=event.researcher,
                data=event.data,
                timestamp=datetime.fromisoformat(event.timestamp)
            )
            session.add(db_event)
            await session.commit()
    import asyncio; asyncio.run(db_task()) 