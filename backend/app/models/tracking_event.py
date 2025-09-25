from app.database.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class TrackingEvent(Base):
    __tablename__ = "tracking_event"

    event_id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, index=True)
    shipment_id = Column(Integer, ForeignKey("shipment.shipment_id"))
    carrier_code = Column(String, index=True)
    location_id = Column(Integer, ForeignKey("location.location_id"))
    status = Column(String(50), nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    raw_payload = Column(JSON, nullable=True)

    shipment = relationship("Shipment", back_populates="events")
    location = relationship("Location", back_populates="events")

    def __repr__(self):
        return f"<TrackingEvent {self.status} at {self.location_id}"


# Every update for a shipment (scanned at Lagos hub, departed warehouse).

# Connected to:

# A shipment.

# A location.
