from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class TrackingEventCreate(BaseModel):
    carrier_code: str
    tracking_id: str
    status: str
    location: Optional[str] = None
    raw_payload: Optional[dict[str, Any]] = None


class TrackingEventResponse(TrackingEventCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
