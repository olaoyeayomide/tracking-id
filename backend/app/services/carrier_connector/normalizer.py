from app.services.carrier_connector.registry import get_connector
from app.schemas.tracking_schema import TrackingResponse


def normalize_from_carrier(
    carrier_code: str, raw_payload: dict, meta: dict | None = None
) -> TrackingResponse:
    connector = get_connector(carrier_code, meta=meta)
    normed = connector.normalize(raw_payload)
    return TrackingResponse(**normed)


def normalize_payload(payload: dict, carrier: str) -> dict:
    """
    Normalize payload from different carriers into a standard format.
    """
    print("Incoming payload:", payload)

    if carrier == "sendbox":
        return {
            "tracking_id": payload.get("tracking_id"),
            "status": payload.get("status"),
            "location": payload.get("location"),
            "carrier": "sendbox",
        }
    elif carrier == "gig":
        return {
            "tracking_id": payload.get("tracking_id"),
            "status": payload.get("status"),
            "location": payload.get("location"),
            "carrier": "gig",
        }
    else:
        print(f"Error: Unsupported carrier: {carrier}")
        raise ValueError(f"Unsupported carrier: {carrier}")
