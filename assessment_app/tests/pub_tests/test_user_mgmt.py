import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from assessment_app.main import app
from assessment_app.repository.database import get_db, SessionLocal
from assessment_app.models.userinfo import UserInfo

client = TestClient(app)

@pytest.fixture(scope="function")
def db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "name": "Test User"
    }

def test_register_user(test_user_data):
    response = client.post("/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert data["name"] == test_user_data["name"]

def test_login_user(test_user_data):
    # Ensure user is registered first
    client.post("/register", json=test_user_data)

    response = client.post("/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.cookies

def test_get_logged_in_user(test_user_data):
    # Register and login to get token
    client.post("/register", json=test_user_data)
    login_resp = client.post("/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_resp.cookies.get("access_token")
    assert token

    # Call /user with token as cookie
    response = client.get("/user", cookies={"access_token": token})
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == test_user_data["email"]
    assert user["username"] == test_user_data["username"]
