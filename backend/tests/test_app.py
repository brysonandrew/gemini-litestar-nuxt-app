import pytest
from litestar.testing import TestClient
from app import app, users, jwt_auth, User

@pytest.fixture(autouse=True)
def reset_users():
    # Reset users for each test to ensure a clean state
    users.clear()
    users[1] = User(id=1, name="John Doe", email="john.doe@example.com")

def test_login_success():
    with TestClient(app=app) as client:
        response = client.post("/login", json={"email": "john.doe@example.com", "password": "anypassword"})
        assert response.status_code == 201
        assert "token" in response.json()

def test_login_failure():
    with TestClient(app=app) as client:
        response = client.post("/login", json={"email": "nonexistent@example.com", "password": "wrongpassword"})
        assert response.status_code == 401  # Litestar returns 401 for invalid credentials
        assert response.json() == {"detail": "Invalid credentials", "status_code": 401}

def test_profile_access_unauthorized():
    with TestClient(app=app) as client:
        response = client.get("/profile")
        assert response.status_code == 401

def test_profile_access_authorized():
    with TestClient(app=app) as client:
        # First, log in to get a token
        login_response = client.post("/login", json={"email": "john.doe@example.com", "password": "anypassword"})
        token = login_response.json()["token"]

        # Then, access the profile with the token
        profile_response = client.get("/profile", headers={
            "Authorization": f"Bearer {token}"
        })
        assert profile_response.status_code == 200
        assert profile_response.json() == {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}
