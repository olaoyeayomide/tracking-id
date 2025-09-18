from app.database.connection import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    customer_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(100))

    preferences = relationship("UserPreference", back_populates="user")
    shipments = relationship("Shipment", back_populates="user")
