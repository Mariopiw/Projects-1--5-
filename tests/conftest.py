import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET", "test-secret")

import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine, SessionLocal
from app.main import app
from app.models import User
from app.security import hash_password


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add_all([
        User(username="operator", hashed_password=hash_password("operator123"), role="operator"),
        User(username="viewer", hashed_password=hash_password("viewer123"), role="viewer"),
    ])
    db.commit(); db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    Path("test.db").unlink(missing_ok=True)


@pytest.fixture
def client():
    return TestClient(app)


def auth_header(client, username="operator", password="operator123"):
    response = client.post("/auth/token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
