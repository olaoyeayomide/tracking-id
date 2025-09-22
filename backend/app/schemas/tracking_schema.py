from pydantic import BaseModel
from typing import Optional


class TrackingRequest(BaseModel):
    tracking_id: str
    status: str
    location: Optional[str] = None


class TrackingResponse(BaseModel):
    tracking_id: str
    status: str
    location: Optional[str] = None
    carrier: str
