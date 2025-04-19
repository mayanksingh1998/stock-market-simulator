from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from assessment_app.schemas.trade import TradeCreate, TradeResponse
from assessment_app.repository.database import get_db
from assessment_app.service.auth_service import get_current_user
from assessment_app.models.userinfo import UserInfo
from assessment_app.service import trade_service

router = APIRouter()

@router.post("/trade", response_model=TradeResponse)
def place_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return trade_service.place_trade_logic(db, trade, current_user)


@router.get("/trades", response_model=List[TradeResponse])
def get_user_trades(
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return trade_service.get_user_trades_logic(db, current_user)
