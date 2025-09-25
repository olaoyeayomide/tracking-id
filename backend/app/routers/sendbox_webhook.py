from fastapi import APIRouter, Request
import logging
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

router = APIRouter()


# ✅ Define the webhook payload schema
class SendboxWebhookPayload(BaseModel):
    event: str
    tracking_id: str
    status: str
    timestamp: datetime
    extra_data: Optional[Dict] = None  # flexible field for courier, recipient, etc.


# ✅ Webhook endpoint
@router.post("/sendbox")
async def sendbox_webhook(payload: SendboxWebhookPayload):
    # just echo it back for now (simulating Sendbox)
    return {"status": "success", "data": payload.dict()}


# @router.post("/webhooks/sendbox")
# async def sendbox_webhook(request: Request):
#     try:
#         payload = await request.json()
#     except Exception:
#         payload = {"error": "No valid JSON body received"}

#     logging.info(f"📦 Sendbox webhook received: {payload}")

#     return {"status": "success", "data": payload}

#     # TODO: process events (e.g. shipment created, shipment updated, delivery complete)
