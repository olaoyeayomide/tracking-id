from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class UserPreference(Base):
    __tablename__ = "user_preference"

    user_pref_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.customer_id"))
    language = Column(String(20))
    subtitle_preference = Column(String(20))
    notification_preferences = Column(String(20))

    user = relationship("User", back_populates="preferences")


# Stores per-user settings like language, subtitle, and notifications.

# Linked back to the User.
