from sqlalchemy.orm import Session
from app.models.tracking_event import TrackingEvent
from app.schemas.tracking_event import TrackingEventCreate


def create_tracking_event(db: Session, event: TrackingEventCreate) -> TrackingEvent:
    db_event = TrackingEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_events_by_tracking_id(db: Session, tracking_id: str):
    return (
        db.query(TrackingEvent).filter(TrackingEvent.tracking_id == tracking_id).all()
    )
