from fastapi import APIRouter, HTTPException
from app.schemas.tracking_schema import TrackingResponse, TrackingRequest
from app.services.carrier_connector.normalizer import normalize_from_carrier
from app.services.carrier_connector.registry import get_connector
from app.services.carrier_connector.gig import get_gig_status


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


@router.get("/track/gig/{tracking_id}")
async def track_gig(tracking_id: str):
    return await get_gig_status(tracking_id)
