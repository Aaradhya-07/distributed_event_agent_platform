from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_user_interaction_event():
    payload = {
        "user_id": "user123",
        "event_type": "page_view",
        "timestamp": "2024-06-27T12:00:00",
        "event_metadata": {"page": "/home", "duration": 30}
    }
    response = client.post("/events/user-interaction", json=payload)
    assert response.status_code == 202

def test_chemical_research_event():
    payload = {
        "molecule_id": "mol123",
        "researcher": "Dr. Smith",
        "data": {"formula": "H2O", "weight": 18.015},
        "timestamp": "2024-06-27T12:00:00"
    }
    response = client.post("/events/chemical-research", json=payload)
    assert response.status_code == 202 