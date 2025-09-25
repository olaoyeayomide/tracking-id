# tests/conftest.py
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the app module is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "")))

from app.database.connection import Base, get_db
from app.main import app
from app.core.config import settings

# Use SQLite file-based DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as c:
        yield c
