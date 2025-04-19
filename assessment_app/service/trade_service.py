from sqlalchemy.orm import Session
from fastapi import HTTPException

from assessment_app.models import Portfolio
from assessment_app.models.constants import TradeType
from assessment_app.models.trade import Trade
from assessment_app.models.holding import Holding
from assessment_app.models.userinfo import UserInfo
from assessment_app.schemas.trade import TradeCreate


def place_trade_logic(
    db: Session, trade: TradeCreate, current_user: UserInfo
) -> Trade:
    if trade.quantity <= 0 or trade.price <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive.")

    portfolio = db.query(Portfolio).filter_by(id=trade.portfolio_id, user_id=current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found for current user.")

    holding = (
        db.query(Holding)
        .join(Portfolio)
        .filter(
            Portfolio.user_id == current_user.id,
            Holding.portfolio_id == trade.portfolio_id,
            Holding.stock_id == trade.stock_id,
        )
        .first()
    )

    if trade.trade_type == TradeType.BUY:
        if holding:
            total_quantity = holding.quantity + trade.quantity
            total_cost = (holding.avg_buy_price * holding.quantity) + (trade.price * trade.quantity)
            holding.avg_buy_price = total_cost / total_quantity
            holding.quantity = total_quantity
        else:
            holding = Holding(
                portfolio_id=trade.portfolio_id,
                stock_id=trade.stock_id,
                quantity=trade.quantity,
                avg_buy_price=trade.price,
            )
            db.add(holding)

    elif trade.trade_type == TradeType.SELL:
        if not holding or holding.quantity < trade.quantity:
            raise HTTPException(status_code=400, detail="Insufficient holdings to sell.")
        holding.quantity -= trade.quantity
        proceeds = trade.quantity * trade.price
        portfolio.cash += proceeds

    else:
        raise HTTPException(status_code=400, detail="Invalid trade type.")

    new_trade = Trade(
        user_id=current_user.id,
        stock_id=trade.stock_id,
    portfolio_id=trade.portfolio_id,
        trade_type=trade.trade_type,
        quantity=trade.quantity,
        price=trade.price,
    )

    db.add(new_trade)
    db.add(holding)
    db.add(portfolio)
    db.commit()
    db.refresh(new_trade)
    return new_trade


def get_user_trades_logic(db: Session, current_user: UserInfo):
    return (
        db.query(Trade)
        .filter(Trade.user_id == current_user.id)
        .order_by(Trade.timestamp.desc())
        .all()
    )
