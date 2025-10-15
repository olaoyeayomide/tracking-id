# app/api/webhooks.py
from fastapi import APIRouter, Request, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import db_dependency
from app.services.carrier_connector.registry import get_connector
from app.services.carrier_connector.normalizer import normalize_payload
from app.crud.tracking_event import create_tracking_event, get_events_by_tracking_id
from app.schemas.sendbox import SendboxWebhookPayload
from app.schemas.tracking_event import TrackingEventResponse, TrackingEventResponseList

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


@router.post("/sendbox", response_model=TrackingEventResponse)
def receive_webhook(payload: SendboxWebhookPayload, db: db_dependency):
    # normalize payload from sendbox
    normalized = normalize_payload(payload.model_dump(), carrier="sendbox")

    # save to DB
    db_event = create_tracking_event(db, normalized)

    return TrackingEventResponse.model_validate(db_event)


@router.get("/{tracking_id}", response_model=TrackingEventResponseList)
def get_tracking_events(tracking_id: str, db: db_dependency):
    """
    Fetch all tracking events for a given tracking_id.
    """
    events = get_events_by_tracking_id(db, tracking_id)
    if not events:
        raise HTTPException(
            status_code=404, detail="No events found for this tracking ID"
        )

    return TrackingEventResponseList(
        tracking_id=tracking_id,
        events=[
            TrackingEventResponse.model_validate(e, from_attributes=True)
            for e in events
        ],
    )
