from app.services.carrier_connector.base import CarrierAdapter
from typing import Dict, Any


class SendboxConnector(CarrierAdapter):
    name = "sendbox"

    def __init__(self, meta: dict | None = None):
        self.meta = meta

    async def fetch_by_api(self, tracking_id: str) -> Dict[str, Any]:
        # placeholder for API fetch
        return {
            "status": "in_transit",
            "location": "Lagos",
            "tracking_id": tracking_id,
        }

    async def fetch_by_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # placeholder for webhook push payload
        return {
            "status": payload.get("status", "unknown"),
            "location": payload.get("location", "unknown"),
            "tracking_id": payload.get("tracking_id", "unknown"),
        }

    async def fetch_by_scraper(self, tracking_id: str) -> Dict[str, Any]:
        # placeholder for scraper
        return {
            "status": "pending",
            "location": "scraper-location",
            "tracking_id": tracking_id,
        }

    def normalize(self, raw_payload: dict) -> dict:
        """
        Normalize Sendbox API response or test payload into TrackingResponse format.
        """
        return {
            "status": raw_payload.get("status", "unknown"),
            "location": raw_payload.get("location", "unknown"),
            "tracking_id": raw_payload.get("tracking_id", "N/A"),
            "carrier": self.name,
        }

    def track(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """For internal tracking endpoint test"""
        return self.normalize(payload)
