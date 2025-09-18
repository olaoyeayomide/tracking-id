from app.database.connection import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class Analytics(Base):
    __tablename__ = "analytics"

    analytics_id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchant.merchant_id"))
    delivery_time = Column(Date, nullable=False)
    on_time_percentage = Column(Date, nullable=False)
    carrier_id = Column(Integer, ForeignKey("carrier.carrier_id"))
    failed_deliveries = Column(Date, nullable=False)
    avg_response_time = Column(Date, nullable=False)

    merchant = relationship("Merchant", back_populates="analytics")


# Stores performance metrics for merchants and carriers.

# Example: delivery time, failed deliveries, response time.

# Linked to Merchant.
