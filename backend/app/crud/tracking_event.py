from sqlalchemy.orm import Session
from app.models.tracking_event import TrackingEvent
from app.models.location import Location
from app.schemas.tracking_event import TrackingEventCreate, TrackingEventResponse
from app.schemas.sendbox import SendboxWebhookPayload


# def create_tracking_event(db: Session, event_in: TrackingEventCreate) -> TrackingEvent:
#     location_obj = None
#     if event_in.location:
#         location_obj = db.query(Location).filter_by(name=event_in.location).first()
#     if not location_obj:
#         location_obj = Location(name=event_in.location)
#         db.add(location_obj)
#         db.commit()
#         db.refresh(location_obj)

#     db_event = TrackingEvent(
#         tracking_id=event_in.tracking_id,
#         status=event_in.status,
#         carrier_code="sendbox",
#         location=location_obj,
#         # location=event_in.location_obj,
#         # raw_payload=event.model_dump(),
#     )
#     db.add(db_event)
#     db.commit()
#     db.refresh(db_event)
#     return db_event


def create_tracking_event(db: Session, normalized: dict) -> TrackingEvent:
    """
    Save a normalized webhook payload as a TrackingEvent in the database.
    """

    # ✅ Map normalized['location'] to location_id
    location_name = normalized.get("location")
    location_obj = None
    if location_name:
        location_obj = db.query(Location).filter_by(name=location_name).first()
        if not location_obj:
            # create location if it does not exist
            location_obj = Location(name=location_name)
            db.add(location_obj)
            db.commit()
            db.refresh(location_obj)

    db_event = TrackingEvent(
        tracking_id=normalized["tracking_id"],
        status=normalized["status"],
        carrier_code=normalized["carrier"],  # ✅ FIXED: use carrier_code
        location_id=location_obj.location_id if location_obj else None,
        raw_payload=normalized,  # store full payload for debugging
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events_by_tracking_id(db: Session, tracking_id: str):
    return (
        db.query(TrackingEvent).filter(TrackingEvent.tracking_id == tracking_id).all()
    )
