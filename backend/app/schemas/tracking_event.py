from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Any, List


class TrackingEventCreate(BaseModel):
    tracking_id: str
    status: str
    location_id: int


class TrackingEventResponse(TrackingEventCreate):
    event_id: int
    tracking_id: str
    carrier_code: str
    location_id: Optional[int] = None
    status: str
    timestamp: datetime
    raw_payload: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class TrackingEventResponseList(BaseModel):
    tracking_id: str
    events: List[TrackingEventResponse]


# class Config:
#     orm_mode = True
#     populate_by_name = True  # ✅ allow using field names or aliases
#     json_encoders = {
#         datetime: lambda v: v.isoformat(),
#     }
#     # ✅ This line ensures the output uses aliases in JSON
#     by_alias = True
