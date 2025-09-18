from app.database.connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Location(Base):
    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    latitude = Column(String(100))
    longitude = Column(String(100))

    events = relationship("TrackingEvent", back_populates="location")


# Stores geographical points (city, lat, long).

# Connected to tracking events.
