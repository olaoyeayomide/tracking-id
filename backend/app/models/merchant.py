from app.database.connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Merchant(Base):
    __tablename__ = "merchant"

    merchant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    api_key = Column(String(50), nullable=False)
    webhook_url = Column(String(200), nullable=False)

    shipments = relationship("Shipment", back_populates="merchant")
    analytics = relationship("Analytics", back_populates="merchant")


# Stores online stores (e.g., Jumia, Amazon).

# api_key + webhook_url → how your system talks back to merchants.

# Linked to shipments and analytics.
