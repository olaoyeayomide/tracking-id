from app.services.carrier_connector.base import CarrierAdapter
from typing import Dict, Any


# class GigConnector(CarrierAdapter):
#     name = "gig"

#     def __init__(self, meta: dict | None = None):
#         self.meta = meta

#     async def fetch_by_api(self, tracking_id: str) -> Dict[str, Any]:
#         # placeholder for API fetch
#         return {
#             "status": "in_transit",
#             "location": "Port Harcourt",
#             "tracking_id": tracking_id,
#         }

#     async def fetch_by_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
#         # placeholder for webhook push payload
#         return {
#             "status": payload.get("status", "unknown"),
#             "location": payload.get("location", "unknown"),
#             "tracking_id": payload.get("tracking_id", "unknown"),
#         }

#     async def fetch_by_scraper(self, tracking_id: str) -> Dict[str, Any]:
#         # placeholder for scraper
#         return {
#             "status": "pending",
#             "location": "scraper-location",
#             "tracking_id": tracking_id,
#         }

#     def normalize(self, raw_payload: dict) -> dict:
#         """
#         Normalize Sendbox API response or test payload into TrackingResponse format.
#         """
#         return {
#             "status": raw_payload.get("status", "unknown"),
#             "location": raw_payload.get("location", "unknown"),
#             "tracking_id": raw_payload.get("tracking_id", "N/A"),
#             "carrier": self.name,
#         }

#     def track(self, payload: Dict[str, Any]) -> Dict[str, Any]:
#         """For internal tracking endpoint test"""
#         return self.normalize(payload)
import httpx


async def get_gig_status(tracking_id: str):
    url = f"https://api.nipost.gov.ng/Track/{tracking_id}"  # Example tracking page
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        status = soup.find("div", {"class": "status"}).text
        location = soup.find("div", {"class": "location"}).text

        return {
            "status": status,
            "location": location,
            "tracking_id": tracking_id,
            "carrier": "gig",
        }
