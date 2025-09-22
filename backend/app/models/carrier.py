from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship


class Carrier(Base):
    __tablename__ = "carrier"
    carrier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(
        String, unique=True, index=True
    )  # Short unique identifier Eg; DHL, SENDBOX
    type = Column(String)  # This type should be false
    base_url = Column(String, nullable=True)
    api_endpoint = Column(String(200), nullable=True)
    auth_config = Column(String(200), nullable=True)
    has_webhook = Column(Boolean, default=False)
    carrier_metadata = Column(JSON, nullable=True)

    shipments = relationship("Shipment", back_populates="carrier")


# Stores shipping carriers (like DHL, UPS, FedEx).

# api_endpoint + auth_config → used to connect to carrier APIs.

# shipments → linked to shipments sent via that carrier.
