from fastapi import FastAPI, HTTPException
from app.database.connection import Base, engine, db_dependency
from app.models import Carrier, Shipment, TrackingEvent
from sqlalchemy.orm import Session

# from app.routers.tracking import router
from app.routers import tracking

app = FastAPI()

# app.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])
# app.include_router(router, prefix="/api", tags=["Tracking"])
app.include_router(tracking.router)
