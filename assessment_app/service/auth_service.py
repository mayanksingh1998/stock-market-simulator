from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from assessment_app.utils.auth import decode_token
from assessment_app.repository.database import SessionLocal
from assessment_app.models.userinfo import UserInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInfo:
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    db = SessionLocal()
    user = db.query(UserInfo).filter(UserInfo.email == email).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
