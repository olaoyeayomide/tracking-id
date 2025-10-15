import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database.connection import Base, engine, db_dependency

# Use TestClient
client = TestClient(app)


# Fixture for database session
@pytest.fixture
def db_session():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()


def test_webhook_post_and_get(db_session):
    payload = {"tracking_id": "TEST123", "status": "in_transit", "location": "Lagos"}

    response = client.post("/api/webhooks/sendbox", json=payload)

    # ✅ Assert status code
    assert response.status_code == 200, f"Response content: {response.content}"

    data = response.json()

    # ✅ Assert all required fields exist
    assert "event_id" in data
    assert "tracking_id" in data
    assert "status" in data
    assert "location_id" in data
    assert "carrier_code" in data
    assert "timestamp" in data

    # ✅ Assert values match
    assert data["tracking_id"] == payload["tracking_id"]
    assert data["status"] == payload["status"]
    assert data["location_id"] is not None
    assert data["carrier_code"] == "sendbox"
    assert "timestamp" in data

    # ✅ GET events by tracking_id
    response_get = client.get(f"/api/webhooks/{payload['tracking_id']}")
    assert response_get.status_code == 200

    response_json = response_get.json()

    # ✅ Updated structure — the response is a dict, not a list
    assert "events" in response_json
    assert len(response_json["events"]) > 0

    first_event = response_json["events"][0]

    # ✅ Validate event details
    assert first_event["tracking_id"] == payload["tracking_id"]
    assert first_event["status"] == payload["status"]
