from app.database.connection import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON


class Cache(Base):
    __tablename__ = "cache"

    cache_id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(
        String(50), nullable=False
    )  # e.g., 'shipment', 'tracking_event'
    entity_id = Column(Integer, nullable=False)  # ID of entity being cached
    data = Column(JSON, nullable=False)  # Cached payload
    expires_at = Column(DateTime(timezone=True))
    last_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # ✅ still correct
        onupdate=func.now(),  # ✅ if you want auto-update
    )


# Stores temporary data to reduce API calls.

# Example:

# If DHL API was called yesterday for a shipment → store the JSON response in cache.

# When user checks again today → load from cache first, not from DHL.

# expires_at → when the cache should be refreshed.
