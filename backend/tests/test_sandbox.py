import pytest
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from app.services.carrier_connector.sendbox import SendboxConnector


@pytest.mark.asyncio
async def test_sendbox_placeholder_fetch():
    connector = SendboxConnector()

    # Call the placeholder fetch method
    result = await connector.fetch_by_api("TEST123")

    # Assertions to make sure the placeholder works
    assert result["tracking_id"] == "TEST123"
    assert result["status"] == "in_transit"
    assert result["location"] == "Lagos"


@pytest.mark.asyncio
async def test_sendbox_normalize():
    connector = SendboxConnector()

    raw_payload = {
        "status": "delivered",
        "location": "Abuja",
        "tracking_id": "DEL123",
    }

    result = connector.normalize(raw_payload)

    expected = {
        "status": "delivered",
        "location": "Abuja",
        "tracking_id": "DEL123",
        "carrier": "sendbox",  # include carrier now
    }

    assert result == expected  # normalization keeps keys consistent
