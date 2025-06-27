from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from shared.config import Settings

settings = Settings()
# Create the async SQLAlchemy engine for PostgreSQL
engine = create_async_engine(settings.postgres_url, echo=True)
# Create a sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Async generator to provide a database session for dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session 