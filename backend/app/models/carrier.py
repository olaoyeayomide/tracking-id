from app.database.connection import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    JSON,
    Enum,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
import datetime
from enum import Enum as PyEnum


class CarrierType(PyEnum):
    API = "API"
    WEBHOOK = "WEBHOOK"
    SCRAPER = "SCRAPER"
    MANUAL = "MANUAL"


class CarrierStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"
    # TESTING = "TESTING"
    # ERROR = "ERROR"


# Reusable SQLAlchemy Enum types
carrier_type_enum = Enum(CarrierType, name="carriertype")
carrier_status_enum = Enum(CarrierStatus, name="carrierstatus")


class Carrier(Base):
    __tablename__ = "carrier"
    carrier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(
        String, unique=True, index=True
    )  # Short unique identifier Eg; DHL, SENDBOX
    description = Column(Text, nullable=True)
    type = Column(carrier_type_enum, default=CarrierType.API, nullable=False)
    status = Column(carrier_status_enum, default=CarrierStatus.ACTIVE, nullable=False)
    base_url = Column(String, nullable=True)

    # API Configuration
    api_endpoint = Column(String(200), nullable=True)
    auth_type = Column(String(50), default="api_key")  # api_key, oauth, basic, none
    auth_config = Column(JSON, nullable=True)

    # Webhook Configuration
    webhook_verification = Column(Boolean, default=False)
    webhook_url = Column(String(255), nullable=True)
    webhook_secret = Column(String(255), nullable=True)

    # Scraper Configuration
    scraper_config = Column(JSON, nullable=True)
    requires_js = Column(Boolean, default=False)

    # Tracking
    tracking_url_template = Column(String(255), nullable=True)
    tracking_id_pattern = Column(String(100), nullable=True)

    # Metadata
    country = Column(String(50), default="Nigeria")
    support_phone = Column(String(20), nullable=True)
    support_email = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    carrier_metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    # Relationship
    shipments = relationship("Shipment", back_populates="carrier")
    webhooks = relationship("CarrierWebhook", back_populates="carrier")

    def __repr__(self):
        return f"<Carrier {self.name} ({self.code})>"

    @property
    def supports_webhook(self):
        return (
            self.type == CarrierType.WEBHOOK
            and self.webhook_url
            and self.webhook_verified
        )

    @property
    def supports_api(self):
        return self.type == CarrierType.API and self.api_endpoint

    @property
    def requires_scraping(self):
        return self.type == CarrierType.SCRAPER


class CarrierWebhook(Base):
    __tablename__ = "carrier_webhooks"

    id = Column(Integer, primary_key=True, index=True)
    carrier_id_ref = Column(Integer, ForeignKey("carrier.carrier_id"), nullable=False)
    event_type = Column(
        String(50), nullable=False
    )  # tracking_update, delivery, exception
    payload = Column(JSON, nullable=False)
    status = Column(String(20), default="pending")  # pending, processed, failed
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime, nullable=True)
    next_attempt = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    carrier = relationship("Carrier", back_populates="webhooks")


# Stores shipping carriers (like DHL, UPS, FedEx).

# api_endpoint + auth_config → used to connect to carrier APIs.

# shipments → linked to shipments sent via that carrier.
