from pydantic import BaseSettings

class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic_user: str = "user_events"
    kafka_topic_chemical: str = "chemical_events"
    postgres_url: str = "postgresql+asyncpg://user:password@localhost:5432/db"
    llm_api_url: str = "http://localhost:8001/llm"
    llm_api_key: str = "dummy-key"

    class Config:
        env_file = ".env"
