import pytest
from app.workers.event_handlers import process_user_event, process_chemical_event
from shared.models import UserInteractionEvent, ChemicalResearchEvent
import json

def test_process_user_event(monkeypatch):
    event = UserInteractionEvent(
        user_id="user123",
        event_type="page_view",
        timestamp="2024-06-27T12:00:00",
        event_metadata={"page": "/home", "duration": 30}
    )
    # Mock DB session
    monkeypatch.setattr("app.workers.event_handlers.AsyncSessionLocal", lambda: None)
    # Should not raise
    process_user_event(event.json())

def test_process_chemical_event(monkeypatch):
    event = ChemicalResearchEvent(
        molecule_id="mol123",
        researcher="Dr. Smith",
        data={"formula": "H2O", "weight": 18.015},
        timestamp="2024-06-27T12:00:00"
    )
    # Mock LLM client and DB session
    monkeypatch.setattr("app.workers.event_handlers.GroqLLMClient.extract_properties", lambda self, data: {"color": "colorless", "pH": 7.0})
    monkeypatch.setattr("app.workers.event_handlers.AsyncSessionLocal", lambda: None)
    # Should not raise
    process_chemical_event(event.json()) 