import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from assessment_app.models.userinfo import UserInfo
from assessment_app.service.auth_service import get_current_user

# Sample payload and token
VALID_TOKEN = "valid.jwt.token"
FAKE_EMAIL = "test@example.com"

@pytest.fixture
def fake_user():
    return UserInfo(id=1, name="Test User", email=FAKE_EMAIL)


def test_get_current_user_success(fake_user):
    with patch("assessment_app.deps.auth.decode_token") as mock_decode, \
         patch("assessment_app.deps.auth.SessionLocal") as mock_session:

        # Mock token decoding
        mock_decode.return_value = {"sub": FAKE_EMAIL}

        # Mock DB session
        mock_db = MagicMock()
        mock_db.query().filter().first.return_value = fake_user
        mock_session.return_value = mock_db

        # Call the dependency directly
        user = get_current_user(token=VALID_TOKEN)

        assert user.email == FAKE_EMAIL
        assert user.name == "Test User"
        mock_db.close.assert_called_once()


def test_get_current_user_invalid_token():
    with patch("assessment_app.deps.auth.decode_token") as mock_decode:
        mock_decode.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=VALID_TOKEN)
        assert exc_info.value.status_code == 401
        assert "Invalid authentication credentials" in exc_info.value.detail


def test_get_current_user_missing_email():
    with patch("assessment_app.deps.auth.decode_token") as mock_decode:
        mock_decode.return_value = {"no_sub": "oops"}

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=VALID_TOKEN)
        assert exc_info.value.status_code == 400
        assert "Invalid token payload" in exc_info.value.detail


def test_get_current_user_user_not_found():
    with patch("assessment_app.deps.auth.decode_token") as mock_decode, \
         patch("assessment_app.deps.auth.SessionLocal") as mock_session:

        mock_decode.return_value = {"sub": FAKE_EMAIL}

        mock_db = MagicMock()
        mock_db.query().filter().first.return_value = None
        mock_session.return_value = mock_db

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=VALID_TOKEN)
        assert exc_info.value.status_code == 404
        assert "User not found" in exc_info.value.detail
        mock_db.close.assert_called_once()
