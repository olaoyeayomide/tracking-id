import requests
from datetime import datetime


# Example function to fetch tracking info from GIG API
def fetch_gig_tracking(tracking_id: str):
    """
    Simulates fetching tracking data from GIG API.
    Replace `api_url` with real GIG endpoint when available.
    """
    api_url = f"https://gig-logistics-api.com/track/{tracking_id}"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Normalize response
        return {
            "carrier": "GIG Logistics",
            "tracking_id": tracking_id,
            "status": data.get("current_status", "Unknown"),
            "location": data.get("current_location", "Unknown"),
            "timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"error": str(e)}
