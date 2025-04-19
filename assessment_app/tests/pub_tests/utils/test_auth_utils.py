import pytest
from datetime import timedelta, datetime
from jose import jwt

from fastapi import HTTPException

from assessment_app.utils import auth

# Use the same constants from auth_utils
SECRET_KEY = auth.SECRET_KEY
ALGORITHM = auth.ALGORITHM


def test_verify_password_success():
    password = "mysecurepassword"
    hashed = auth.pwd_context.hash(password)
    assert auth.verify_password(password, hashed) is True


def test_verify_password_failure():
    password = "mysecurepassword"
    wrong_password = "wrongpassword"
    hashed = auth.pwd_context.hash(password)
    assert auth.verify_password(wrong_password, hashed) is False


def test_create_access_token_and_decode_token_success():
    data = {"sub": "testuser"}
    token = auth.create_access_token(data)

    decoded = auth.decode_token(token)
    assert decoded["sub"] == "testuser"
    assert "exp" in decoded


def test_create_access_token_with_custom_expiry():
    data = {"sub": "testuser"}
    expiry = timedelta(minutes=5)
    token = auth.create_access_token(data, expires_delta=expiry)

    decoded = auth.decode_token(token)
    assert decoded["sub"] == "testuser"


def test_decode_token_expired():
    data = {"sub": "expireduser"}
    expired_time = datetime.utcnow() - timedelta(minutes=1)
    token = jwt.encode({**data, "exp": expired_time}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        auth.decode_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token has expired"


def test_decode_token_invalid_signature():
    data = {"sub": "tampereduser"}
    token = jwt.encode(data, "wrongsecret", algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        auth.decode_token(token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
