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
