from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from assessment_app.schemas.backtest import BacktestRequest, BacktestResponse
from assessment_app.service.auth_service import get_current_user
from assessment_app.repository import database
from assessment_app.service import backtest_service
from assessment_app.models.userinfo import UserInfo

router = APIRouter()

@router.post("/backtest", response_model=BacktestResponse)
def backtest_strategy_route(
    request: BacktestRequest,
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return backtest_service.backtest_strategy(request, db, current_user.id)
