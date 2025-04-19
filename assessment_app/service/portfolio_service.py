from datetime import date
from sqlalchemy.orm import Session

from assessment_app.models import Portfolio, StockPrice, Holding
from assessment_app.schemas.portfolio import PortfolioRequest
from assessment_app.schemas.holding import HoldingResponse
from fastapi import HTTPException

def get_user_portfolios(db: Session, user_id: int):
    portfolios = db.query(Portfolio).filter_by(user_id=user_id).all()

    for portfolio in portfolios:
        daily_pnl = 0.0
        for holding in portfolio.holdings:
            prices = (
                db.query(StockPrice)
                .filter(StockPrice.stock_id == holding.stock_id, StockPrice.date >= date.today())
                .order_by(StockPrice.date.asc())
                .all()
            )
            if len(prices) >= 2:
                open_price = prices[0].open
                close_price = prices[-1].close
                daily_pnl += (close_price - open_price) * holding.quantity
        portfolio.daily_pnl = daily_pnl

    return portfolios


def create_portfolio(db: Session, user_id: int, req: PortfolioRequest):
    portfolio = Portfolio(
        name=req.name,
        cash=req.initial_funds,
        user_id=user_id,
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def get_portfolio_by_id(db: Session, portfolio_id: str, user_id: int):
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    pnl = 0.0
    holding_responses = []

    for holding in portfolio.holdings:
        latest_price = (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == holding.stock_id, StockPrice.date == date.today())
            .order_by(StockPrice.date.desc())
            .first()
        )
        if latest_price:
            current_value = latest_price.close * holding.quantity
            avg_cost = holding.avg_buy_price * holding.quantity
            holding_pnl = round(current_value - avg_cost, 2)
            pnl += current_value - avg_cost
        else:
            holding_pnl = 0.0

        holding_responses.append(HoldingResponse(
            id=holding.id,
            portfolio_id=holding.portfolio_id,
            stock_id=holding.stock_id,
            quantity=holding.quantity,
            avg_buy_price=holding.avg_buy_price,
            pnl=holding_pnl,
        ))

    return {
        "portfolio": portfolio,
        "holdings": holding_responses,
        "daily_pnl": round(pnl, 2),
    }


def get_holdings(db: Session, portfolio_id: int):
    holdings = db.query(Holding).filter_by(portfolio_id=portfolio_id).all()

    for holding in holdings:
        latest_price = (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == holding.stock_id, StockPrice.date == date.today())
            .order_by(StockPrice.date.desc())
            .first()
        )
        holding.pnl = round(
            (latest_price.close - holding.avg_buy_price) * holding.quantity,
            2
        ) if latest_price else 0.0

    return holdings
