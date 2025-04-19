from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from assessment_app.service.auth_service import get_current_user
from assessment_app.models import UserInfo
from assessment_app.repository.database import get_db
from assessment_app.schemas.user import UserResponse, UserCreate
from assessment_app.service import user_mgmt

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return user_mgmt.register_user_service(user, db)

@router.post("/login", response_model=str)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> JSONResponse:
    token = user_mgmt.login_user_service(form_data.username, form_data.password, db)
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.get("/user", response_model=UserResponse)
async def get_logged_in_user(current_user: UserInfo = Depends(get_current_user)):
    return current_user
