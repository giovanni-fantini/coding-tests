import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, get_db, engine_factory

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = engine_factory(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a fixture for setting up the database
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create the tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: Drop the tables
    Base.metadata.drop_all(bind=engine)

# Create a fixture for the FastAPI test client
@pytest.fixture(scope="module")
def client(setup_database):
    return TestClient(app)

# Create a fixture for the database session
@pytest.fixture
def db_session(setup_database):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()