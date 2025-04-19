from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from assessment_app.models import UserInfo
from assessment_app.repository.database import get_db
from assessment_app.service.auth_service import get_current_user
from assessment_app.service.analysis_service import (
    get_stock_cagr_return,
    get_portfolio_cagr_return,
)

router = APIRouter()


@router.get("/analysis/estimate_returns/stock", response_model=float)
async def get_stock_analysis(
    stock_symbol: str,
    start_ts: datetime,
    end_ts: datetime,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user)  # now correctly typed
) -> float:
    return get_stock_cagr_return(stock_symbol, start_ts, end_ts, db)

@router.get("/analysis/estimate_returns/portfolio")
async def estimate_portfolio_returns(
    start_ts: datetime,
    end_ts: datetime,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return get_portfolio_cagr_return(current_user.id, start_ts, end_ts, db)
