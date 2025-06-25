from fastapi import FastAPI
from shared.config import Settings

app = FastAPI(title="Event Subscriber Service")
settings = Settings()

@app.get("/health")
async def health_check():
    return {"status": "ok"} 