from datetime import datetime
from sqlalchemy.orm import Session

from assessment_app.models.stock import Stock
from assessment_app.models.stock_price import StockPrice
from assessment_app.models.portfolio import Portfolio
from assessment_app.models.holding import Holding
from assessment_app.utils.utils import compute_cagr
from fastapi import HTTPException, status


def get_stock_cagr_return(
    stock_symbol: str,
    start_ts: datetime,
    end_ts: datetime,
    db: Session
) -> float:
    stock = db.query(Stock).filter(Stock.symbol == stock_symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    start_price_entry = (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock.id, StockPrice.date <= start_ts.date())
        .order_by(StockPrice.date.desc())
        .first()
    )
    print("start_price_entry:", start_price_entry)

    end_price_entry = (
        db.query(StockPrice)
        .filter(StockPrice.stock_id == stock.id, StockPrice.date <= end_ts.date())
        .order_by(StockPrice.date.desc())
        .first()
    )

    print("end_price_entry:", end_price_entry)


    if not start_price_entry or not end_price_entry:
        raise HTTPException(status_code=404, detail="Stock prices not available for given timestamps")

    return compute_cagr(start_price_entry.open, end_price_entry.close, start_ts, end_ts)


def get_portfolio_cagr_return(
    user_id: int,
    start_ts: datetime,
    end_ts: datetime,
    db: Session
) -> float:
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
    if not portfolios:
        raise HTTPException(status_code=404, detail="User has no portfolios")

    total_start_value = 0
    total_end_value = 0

    for portfolio in portfolios:
        holdings = db.query(Holding).filter(Holding.portfolio_id == portfolio.id).all()
        for holding in holdings:
            stock_id = holding.stock_id

            start_price_entry = (
                db.query(StockPrice)
                .filter(StockPrice.stock_id == stock_id, StockPrice.date <= start_ts)
                .order_by(StockPrice.date.desc())
                .first()
            )

            end_price_entry = (
                db.query(StockPrice)
                .filter(StockPrice.stock_id == stock_id, StockPrice.date <= end_ts)
                .order_by(StockPrice.date.desc())
                .first()
            )

            if not start_price_entry or not end_price_entry:
                continue  # skip this holding

            total_start_value += holding.quantity * start_price_entry.open
            total_end_value += holding.quantity * end_price_entry.close

    if total_start_value == 0:
        raise HTTPException(status_code=400, detail="Start portfolio value is zero, cannot compute CAGR")

    return compute_cagr(total_start_value, total_end_value, start_ts, end_ts)
