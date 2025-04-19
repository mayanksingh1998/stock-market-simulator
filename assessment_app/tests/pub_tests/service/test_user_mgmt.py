import pytest
from sqlalchemy.orm import Session

from assessment_app.schemas.user import UserCreate
from assessment_app.tests.pub_tests.utils import create_test_db
from assessment_app.utils.auth import verify_password, create_access_token
from assessment_app.models.userinfo import UserInfo
from assessment_app.service import user_mgmt

@pytest.fixture
def db():
    return create_test_db()

def test_register_user_success(db: Session):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="strongpassword",
        name="Test User"
    )

    user = user_mgmt.register_user_service(user_data, db)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.hashed_password != "strongpassword"  # Should be hashed

def test_register_user_duplicate_email(db: Session):
    user1 = UserCreate(
        username="user1",
        email="duplicate@example.com",
        password="pass123",
        name="User One"
    )
    user2 = UserCreate(
        username="user2",
        email="duplicate@example.com",
        password="pass456",
        name="User Two"
    )
    user_mgmt.register_user_service(user1, db)

    with pytest.raises(Exception) as exc:
        user_mgmt.register_user_service(user2, db)
    assert "Email already registered" in str(exc.value)

def test_register_user_duplicate_username(db: Session):
    user1 = UserCreate(
        username="duplicateuser",
        email="user1@example.com",
        password="pass123",
        name="User One"
    )
    user2 = UserCreate(
        username="duplicateuser",
        email="user2@example.com",
        password="pass456",
        name="User Two"
    )
    user_mgmt.register_user_service(user1, db)

    with pytest.raises(Exception) as exc:
        user_mgmt.register_user_service(user2, db)
    assert "Username already taken" in str(exc.value)

def test_login_user_success(db: Session):
    # Register first
    user_data = UserCreate(
        username="loginuser",
        email="login@example.com",
        password="loginpass",
        name="Login User"
    )
    user_mgmt.register_user_service(user_data, db)

    # Login with correct credentials
    token = user_mgmt.login_user_service("login@example.com", "loginpass", db)
    assert isinstance(token, str)
    assert len(token) > 0

def test_login_user_invalid_email(db: Session):
    with pytest.raises(Exception) as exc:
        user_mgmt.login_user_service("nonexistent@example.com", "any", db)
    assert "Invalid credentials" in str(exc.value)

def test_login_user_invalid_password(db: Session):
    user_data = UserCreate(
        username="wrongpass",
        email="wrongpass@example.com",
        password="correctpass",
        name="Wrong Pass"
    )
    user_mgmt.register_user_service(user_data, db)

    with pytest.raises(Exception) as exc:
        user_mgmt.login_user_service("wrongpass@example.com", "wrongpass", db)
    assert "Invalid credentials" in str(exc.value)
