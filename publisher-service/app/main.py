from fastapi import FastAPI
from shared.config import Settings
from app.api import events

app = FastAPI(title="Event Publisher Service")
settings = Settings()

app.include_router(events.router, prefix="/events")

@app.get("/health")
async def health_check():
    return {"status": "ok"} 