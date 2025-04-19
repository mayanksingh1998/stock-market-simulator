from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from assessment_app.models.userinfo import UserInfo
from assessment_app.schemas.user import UserCreate
from assessment_app.utils.auth import verify_password, create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user_service(user: UserCreate, db: Session) -> UserInfo:
    if db.query(UserInfo).filter(UserInfo.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(UserInfo).filter(UserInfo.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = pwd_context.hash(user.password)
    new_user = UserInfo(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user_service(email: str, password: str, db: Session) -> str:
    user = db.query(UserInfo).filter(UserInfo.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return create_access_token(data={"sub": user.email})
