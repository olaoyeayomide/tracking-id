from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base


class Shipment(Base):
    __tablename__ = "shipment"

    shipment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.customer_id"))
    merchant_id = Column(Integer, ForeignKey("merchant.merchant_id"))
    carrier_tracking_id = Column(String(50), nullable=False)
    universal_id = Column(String(50), nullable=False)
    carrier_id = Column(Integer, ForeignKey("carrier.carrier_id"))
    status = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_update = Column(DateTime(timezone=True))
    expected_delivery = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="shipments")
    merchant = relationship("Merchant", back_populates="shipments")
    carrier = relationship("Carrier", back_populates="shipments")
    events = relationship("TrackingEvent", back_populates="shipment")
    notifications = relationship("Notification", back_populates="shipment")

    def __repr__(self):
        return f"<Shipment(id={self.shipment_id}, tracking_id={self.carrier_tracking_id}, status={self.status})>"


# This is the core table 🏆.

# Connects User, Merchant, and Carrier.

# Has:

# carrier_tracking_id (from DHL/UPS/etc).

# universal_id (your own unified tracking ID).

# status (e.g., in transit, delivered).

# created_at, expected_delivery.

# Relationships:

# user → the buyer.

# merchant → the seller.

# carrier → the courier company.

# events → tracking events (locations + statuses).

# notifications → alerts sent to the user.
