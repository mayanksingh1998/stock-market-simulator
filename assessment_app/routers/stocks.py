from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from assessment_app.repository import database
from assessment_app.schemas.stock import StockCreate, StockResponse
from assessment_app.service.auth_service import get_current_user
from assessment_app.models.userinfo import UserInfo
from assessment_app.service import stock_service

router = APIRouter()

@router.post("/stocks", response_model=StockResponse)
def create_stock(
    stock: StockCreate,
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    return stock_service.create_stock_logic(db, stock, current_user)


@router.get("/stocks", response_model=List[StockResponse])
def get_stocks(
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user)
):
    return stock_service.get_stocks_logic(db, current_user)
