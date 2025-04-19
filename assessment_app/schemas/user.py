from __future__ import annotations

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
