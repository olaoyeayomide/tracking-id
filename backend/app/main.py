from fastapi import FastAPI, HTTPException
from app.database.connection import Base, engine, db_dependency
from app.models import Carrier, Shipment, TrackingEvent
from sqlalchemy.orm import Session

from app.routers import tracking
from app.routers import webhooks

app = FastAPI()

app.include_router(tracking.router)
app.include_router(webhooks.router)
