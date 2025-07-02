import pytest
from litestar.testing import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from unittest.mock import patch

# Import necessary components from app and database
from app import Litestar, get, post, Request, jwt_auth, User, LoginData, RegisterData, LoginDTO, pwd_context, NotAuthorizedException, cors_config, retrieve_user_handler, login, register, get_profile
from database import Base, User as DBUser, get_db
from litestar.di import Provide # Ensure Provide is imported

@pytest.fixture(name="db_session")
def db_session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(name="test_client")
def test_client_fixture(db_session):
    # Use patch to temporarily replace the get_db function
    with patch('database.get_db', return_value=iter([db_session])) as mock_get_db:
        # Create a fresh Litestar app instance for testing
        test_app = Litestar(
            route_handlers=[login, register, get_profile],
            on_app_init=[jwt_auth.on_app_init],
            cors_config=cors_config,
            dependencies={
                "db": Provide(mock_get_db) # Use the mocked get_db here
            }
        )
        with TestClient(app=test_app) as client:
            yield client

def test_login_success(test_client, db_session):
    hashed_password = pwd_context.hash("anypassword")
    new_user = DBUser(name="John Doe", email="john.doe@example.com", hashed_password=hashed_password)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    response = test_client.post("/login", json={"email": "john.doe@example.com", "password": "anypassword"})
    assert response.status_code == 201
    assert "token" in response.json()

def test_login_failure(test_client):
    response = test_client.post("/login", json={"email": "nonexistent@example.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials", "status_code": 401}

def test_profile_access_unauthorized(test_client):
    response = test_client.get("/profile")
    assert response.status_code == 401

def test_profile_access_authorized(test_client, db_session):
    hashed_password = pwd_context.hash("anypassword")
    new_user = DBUser(name="John Doe", email="john.doe@example.com", hashed_password=hashed_password)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    login_response = test_client.post("/login", json={"email": "john.doe@example.com", "password": "anypassword"})
    token = login_response.json()["token"]

    profile_response = test_client.get("/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert profile_response.status_code == 200
    assert profile_response.json() == {"id": new_user.id, "name": new_user.name, "email": new_user.email}
