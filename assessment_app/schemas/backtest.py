from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class StrategyName(str, Enum):
    moving_average = "moving_average"
    buy_and_hold = "buy_and_hold"

class BacktestRequest(BaseModel):
    strategy_id: str
    portfolio_id: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    strategy_name: StrategyName = StrategyName.moving_average

class TradeOut(BaseModel):
    id: int
    portfolio_id: str
    stock_id: int
    trade_type: str
    price: float
    quantity: int
    timestamp: datetime

    class Config:
        from_attributes = True  # ✅ Required for .from_orm in Pydantic v2

class BacktestResponse(BaseModel):
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float
    trades: List[TradeOut]
    profit_loss: float
    annualized_return: float