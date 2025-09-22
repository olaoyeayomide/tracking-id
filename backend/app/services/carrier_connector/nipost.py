import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_nipost_tracking(tracking_id: str):
    """
    Scrapes tracking status from NIPOST (since no official API).
    """
    url = f"https://www.nipost.gov.ng/Track/{tracking_id}"  # Example tracking page
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # This will depend on actual HTML structure of NIPOST page
        status_elem = soup.find("div", {"class": "status"})
        location_elem = soup.find("div", {"class": "location"})

        status_text = status_elem.text.strip() if status_elem else "Unknown"
        location_text = location_elem.text.strip() if location_elem else "Unknown"

        return {
            "carrier": "NIPOST",
            "tracking_id": tracking_id,
            "status": status_text,
            "location": location_text,
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}


# services/nipost_service.py

from fastapi import HTTPException

# Mock NiPost data
fake_nipost_data = {
    "NIPOST987654321": {
        "tracking_id": "NIPOST987654321",
        "carrier": "NiPost",
        "status": "Delivered",
        "last_update": "2025-09-13T14:15:00Z",
        "origin": {"city": "Ibadan", "country": "Nigeria"},
        "destination": {"city": "Port Harcourt", "country": "Nigeria"},
        "estimated_delivery": "2025-09-13T14:00:00Z",
        "events": [
            {
                "date": "2025-09-11T09:10:00Z",
                "location": "Ibadan Office",
                "status": "Parcel accepted",
            },
            {
                "date": "2025-09-12T12:00:00Z",
                "location": "Enugu Transit",
                "status": "In transit",
            },
            {
                "date": "2025-09-13T14:15:00Z",
                "location": "Port Harcourt Office",
                "status": "Delivered to recipient",
            },
        ],
    }
}


# def get_nipost_tracking(tracking_id: str):
#     if tracking_id in fake_nipost_data:
#         return fake_nipost_data[tracking_id]
#     raise HTTPException(status_code=404, detail="NiPost tracking ID not found")
