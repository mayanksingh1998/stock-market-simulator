from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from assessment_app.models import Portfolio, Trade, Holding, Stock, StockPrice
from assessment_app.schemas.backtest import (
    BacktestRequest,
    BacktestResponse,
    TradeOut,
    StrategyName,
)
from assessment_app.strategy.buy_and_hold import BuyAndHoldStrategy
from assessment_app.strategy.ma_crossover import MovingAverageCrossoverStrategy


def reset_portfolio(db: Session, portfolio_id: int, initial_capital: float):
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    portfolio.cash = initial_capital
    db.query(Trade).filter_by(portfolio_id=portfolio.id).delete()
    for holding in portfolio.holdings:
        holding.quantity = 0
        holding.avg_buy_price = 0.0
        db.add(holding)
    db.commit()
    return portfolio


def backtest_strategy(request: BacktestRequest, db: Session, user_id: int) -> BacktestResponse:
    portfolio = (
        db.query(Portfolio)
        .filter_by(id=request.portfolio_id, user_id=user_id)
        .first()
    )
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Reset portfolio state
    reset_portfolio(db, portfolio.id, request.initial_capital)

    # Ensure all stocks have holdings in the portfolio
    existing_holding_stock_ids = {h.stock_id for h in portfolio.holdings}
    all_stocks = db.query(Stock).all()

    for stock in all_stocks:
        if stock.id not in existing_holding_stock_ids:
            holding = Holding(
                portfolio_id=portfolio.id,
                stock_id=stock.id,
                quantity=0,
                avg_buy_price=0.0,
            )
            db.add(holding)

    db.commit()

    # Select strategy
    if request.strategy_name == StrategyName.buy_and_hold:
        portfolio = reset_portfolio(db, request.portfolio_id, request.initial_capital)
        strategy_class = BuyAndHoldStrategy
    elif request.strategy_name == StrategyName.moving_average:
        portfolio = reset_portfolio(db, request.portfolio_id, request.initial_capital)
        strategy_class = MovingAverageCrossoverStrategy
    else:
        raise HTTPException(status_code=400, detail="Unsupported strategy")

    # Simulate day by day
    current_date = request.start_date.date()
    end_date = request.end_date.date()

    while current_date <= end_date:
        strategy = strategy_class(db=db, portfolio=portfolio, current_date=current_date)
        strategy.run()
        db.commit()
        current_date += timedelta(days=1)

    # Final output
    trades = db.query(Trade).filter_by(portfolio_id=portfolio.id).all()
    trade_out_list = [TradeOut.from_orm(trade) for trade in trades]

    final_cash = portfolio.cash
    final_holdings_value = 0.0

    for holding in portfolio.holdings:
        latest_price = (
            db.query(StockPrice)
            .filter_by(stock_id=holding.stock_id, date=request.end_date.date())
            .first()
        )
        if latest_price:
            final_holdings_value += holding.quantity * latest_price.close

    final_capital = round(final_cash + final_holdings_value, 2)
    profit_loss = round(final_capital - request.initial_capital, 2)
    num_days = (request.end_date - request.start_date).days

    annualized_return = (
        ((final_capital / request.initial_capital) ** (365 / num_days) - 1)
        if num_days > 0 else 0.0
    )

    return BacktestResponse(
        start_date=request.start_date,
        end_date=request.end_date,
        initial_capital=request.initial_capital,
        final_capital=final_capital,
        trades=trade_out_list,
        profit_loss=profit_loss,
        annualized_return=round(annualized_return * 100, 2)
    )

def reset_portfolio(db, portfolio_id: int, initial_capital: float):
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    portfolio.cash = initial_capital
    db.query(Trade).filter_by(portfolio_id=portfolio.id).delete()
    for holding in portfolio.holdings:
        holding.quantity = 0
        holding.avg_buy_price = 0.0
        db.add(holding)
    db.commit()
    return portfolio