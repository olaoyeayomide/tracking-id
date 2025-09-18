from app.database.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipment.shipment_id"))
    channel = Column(String(50), nullable=False)
    message = Column(String(255), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    shipment = relationship("Shipment", back_populates="notifications")


# Stores notifications sent to users (e.g., SMS, email).

# Linked to a shipment.
