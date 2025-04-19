
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from assessment_app.repository import database
from assessment_app.service import portfolio_service
from assessment_app.service.auth_service import get_current_user
from assessment_app.models.userinfo import UserInfo
from assessment_app.schemas.portfolio import (
    PortfolioResponse, PortfolioRequest, PortfolioDetailResponse, StockHolding
)
from assessment_app.schemas.holding import HoldingResponse

router = APIRouter()

@router.get("/portfolio", response_model=List[PortfolioResponse])
def get_user_portfolios(
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return portfolio_service.get_user_portfolios(db, current_user.id)

@router.post("/portfolio", response_model=PortfolioResponse)
def create_portfolio(
    portfolio_request: PortfolioRequest,
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return portfolio_service.create_portfolio(db, current_user.id, portfolio_request)

@router.get("/portfolio/{portfolio_id}", response_model=PortfolioDetailResponse)
def get_portfolio_by_id(
    portfolio_id: str,
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    result = portfolio_service.get_portfolio_by_id(db, portfolio_id, current_user.id)
    portfolio = result["portfolio"]

    return PortfolioDetailResponse(
        id=portfolio.id,
        name=portfolio.name,
        cash=portfolio.cash,
        created_at=portfolio.created_at,
        current_ts=portfolio.current_ts,
        holdings=result["holdings"],
        daily_pnl=result["daily_pnl"],
    )

@router.get("/portfolio/{portfolio_id}/holdings", response_model=List[HoldingResponse])
def get_holdings_for_portfolio(
    portfolio_id: int,
    db: Session = Depends(database.get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    return portfolio_service.get_holdings(db, portfolio_id)
