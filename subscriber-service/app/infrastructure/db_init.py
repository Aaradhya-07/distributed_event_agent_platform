import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from shared.models import Base
from app.infrastructure.db import engine
import asyncio

async def init_db():
    """Initialize the database by creating all tables defined in the models."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    # Run the database initialization asynchronously
    asyncio.run(init_db()) 