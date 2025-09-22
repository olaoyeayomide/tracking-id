from app.services.carrier_connector.registry import get_connector
from app.schemas.tracking_schema import TrackingResponse


def normalize_from_carrier(
    carrier_code: str, raw_payload: dict, meta: dict | None = None
) -> TrackingResponse:
    connector = get_connector(carrier_code, meta=meta)
    normed = connector.normalize(raw_payload)
    return TrackingResponse(**normed)
