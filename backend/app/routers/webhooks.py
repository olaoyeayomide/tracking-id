# app/api/webhooks.py
from fastapi import APIRouter, Request, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import db_dependency
from app.services.carrier_connector.registry import get_connector
from app.crud.tracking_event import create_tracking_event, get_events_by_tracking_id
from app.schemas.tracking_event import TrackingEventCreate, TrackingEventResponse

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.post("/webhooks/{carrier_code}", response_model=TrackingEventResponse)
async def receive_webhook(carrier_code: str, request: Request, db: db_dependency):
    payload = await request.json()

    try:
        connector = get_connector(carrier_code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Unsupported carrier") from exc

    # Normalize payload
    normalized = connector.normalize(payload)

    # Persist event
    event_data = TrackingEventCreate(
        carrier_code=carrier_code.upper(),
        tracking_id=normalized["tracking_id"],
        status=normalized["status"],
        location=normalized.get("location"),
        raw_payload=payload,
    )
    saved_event = create_tracking_event(db, event_data)
    return saved_event


@router.get("/webhook/{tracking_id}", response_model=List[TrackingEventResponse])
def get_tracking_events(tracking_id: str, db: db_dependency):
    events = get_events_by_tracking_id(db, tracking_id)
    if not events:
        raise HTTPException(
            status_code=404, detail="No events found for this tracking ID"
        )
    return events
