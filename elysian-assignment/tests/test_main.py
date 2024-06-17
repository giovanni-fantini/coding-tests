from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_accept_webhook_add(client, db_session, db_clear):
    payload = {
        "payload_type": "PersonAdded",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "name": "Test User",
            "timestamp": "2023-10-10T12:34:56Z"
        }
    }
    response = client.post("/accept_webhook", json=payload)
    assert response.status_code == 200
    assert response.json() == {"detail": "Webhook processed successfully"}

def test_accept_webhook_rename(client, db_session, db_clear):
    payload_add = {
        "payload_type": "PersonAdded",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "name": "Test User",
            "timestamp": "2023-10-10T12:34:56Z"
        }
    }
    client.post("/accept_webhook", json=payload_add)

    payload_rename = {
        "payload_type": "PersonRenamed",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "name": "Updated User",
            "timestamp": "2023-10-11T12:34:56Z"
        }
    }

    response = client.post("/accept_webhook", json=payload_rename)
    assert response.status_code == 200
    assert response.json() == {"detail": "Webhook processed successfully"}

def test_accept_webhook_remove(client, db_session, db_clear):
    payload_add = {
        "payload_type": "PersonAdded",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "name": "Test User",
            "timestamp": "2023-10-10T12:34:56Z"
        }
    }
    client.post("/accept_webhook", json=payload_add)

    payload_remove = {
        "payload_type": "PersonRemoved",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "timestamp": "2023-10-12T12:34:56Z"
        }
    }
    response = client.post("/accept_webhook", json=payload_remove)
    assert response.status_code == 200
    assert response.json() == {"detail": "Webhook processed successfully"}

def test_get_name(client, db_session, db_clear):
    payload_add = {
        "payload_type": "PersonAdded",
        "payload_content": {
            "person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022",
            "name": "Test User",
            "timestamp": "2023-10-10T12:34:56Z"
        }
    }
    client.post("/accept_webhook", json=payload_add)

    response = client.get("/get_name", params={"person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022"})
    assert response.status_code == 200
    assert response.json() == {"name": "Test User"}

def test_get_name_not_found(client, db_session, db_clear):
    response = client.get("/get_name", params={"person_id": "cd77cd08-2e66-4992-9b6d-d22957f96022"})
    assert response.status_code == 404  # Adjust response code as per your logic
    assert response.json() == {"detail": "Person not found"}