# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from fastapi.testclient import TestClient
# from app.main import app
# from app.db import Base, get_db

# # Test-specific Database URL
# settings.database_url = "sqlite:///./test.db"

# # Create the SQLite engine
# engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Override the dependency to use the test database
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# # Create a fixture for the client
# @pytest.fixture(scope="module")
# def client():
#     # Setup
#     Base.metadata.create_all(bind=engine)
#     test_client = TestClient(app)
    
#     yield test_client  # Testing happens here
    
#     # Teardown
#     Base.metadata.drop_all(bind=engine)

# @pytest.fixture(scope="module")
# def db_session():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()