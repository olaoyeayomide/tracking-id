from pydantic import BaseModel
from typing import Optional


class SendboxWebhookPayload(BaseModel):
    tracking_id: str
    status: str
    location: Optional[str] = None
