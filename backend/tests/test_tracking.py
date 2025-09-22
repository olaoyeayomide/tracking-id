import pytest
from fastapi.testclient import TestClient
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_payload():
    return {
        "status": "in_transit",
        "location": "Lagos",
        "tracking_id": "NIPOST987654321",
    }


def test_track_with_sendbox(sample_payload):
    response = client.post("/tracking/SENDBOX/track", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_transit"
    assert data["location"] == "Lagos"
    assert data["tracking_id"] == "NIPOST987654321"


def test_track_with_gig(sample_payload):
    # GIG is just placeholder for now, returns same normalized structure
    response = client.post("/tracking/GIG/track", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "tracking_id" in data


def test_invalid_carrier(sample_payload):
    response = client.post("/tracking/UNKNOWN/track", json=sample_payload)
    assert response.status_code == 500  # ValueError raised in registry
