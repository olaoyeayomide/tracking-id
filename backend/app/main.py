from fastapi import FastAPI, HTTPException
from app.database.connection import Base, engine
from app.services.carrier_connector.gig import fetch_gig_tracking
from app.services.carrier_connector.nipost import fetch_nipost_tracking

app = FastAPI()


# Simple carrier resolver
def resolve_carrier(tracking_id: str):
    """Decide which carrier to use based on tracking_id format."""
    if tracking_id.startswith("GIG"):  # Example: GIG12345
        return "gig"
    elif tracking_id.startswith("NIPOST"):  # Example: NIPOST12345
        return "nipost"
    else:
        return None


@app.get("/track/{tracking_id}")
def track_shipment(tracking_id: str):
    carrier = resolve_carrier(tracking_id)
    if not carrier:
        raise HTTPException(
            status_code=400, detail="Unsupported carrier or invalid tracking ID format."
        )

    if carrier == "gig":
        result = fetch_gig_tracking(tracking_id)
    elif carrier == "nipost":
        result = fetch_nipost_tracking(tracking_id)
    else:
        raise HTTPException(status_code=400, detail="Unsupported carrier.")

    return result
