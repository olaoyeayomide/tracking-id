# api/track.py

# from fastapi import APIRouter
# from app.services.carrier_connector.sendbox import get_sendbox_tracking
# from app.services.carrier_connector.nipost import get_nipost_tracking

# router = APIRouter()


# @router.get("/track/{tracking_id}")
# async def track_shipment(tracking_id: str):
#     if tracking_id.startswith("SBOX"):
#         return get_sendbox_tracking(tracking_id)
#     elif tracking_id.startswith("NIPOST"):
#         return get_nipost_tracking(tracking_id)
#     return {"detail": "Unsupported carrier"}

# api/track.py

from fastapi import APIRouter, HTTPException
from app.schemas.tracking_schema import TrackingResponse, TrackingRequest
from app.services.carrier_connector.normalizer import normalize_from_carrier
from app.services.carrier_connector.registry import get_connector


# router = APIRouter()

router = APIRouter(prefix="/tracking", tags=["Tracking"])


@router.post("/{carrier_code}/track", response_model=TrackingResponse)
def track_package(carrier_code: str, payload: TrackingRequest):
    try:
        print(f"Incoming payload: {payload.model_dump()}")
        connector = get_connector(carrier_code)  # <-- get the proper connector
        tracked = connector.track(payload.model_dump())  # use normalize
        print(f"Normalized output: {tracked}")
        return TrackingResponse(**tracked)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
