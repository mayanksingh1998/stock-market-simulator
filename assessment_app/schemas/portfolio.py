from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from assessment_app.schemas.holding import HoldingResponse


class StockHolding(BaseModel):
    symbol: str
    name: str
    quantity: int
    current_price: float
    average_buy_price: float
    value: float
    returns: float
    returns_percentage: float


class PortfolioRequest(BaseModel):
    name: str
    initial_funds: float


class PortfolioResponse(BaseModel):
    id: str
    user_id: int
    name: str
    cash: float
    created_at: datetime
    current_ts: datetime
    holdings: List[HoldingResponse] = []
    daily_pnl: Optional[float] = 0.0

    class Config:
        from_attributes = True

class PortfolioDetailResponse(BaseModel):
    id: str
    name: str
    cash: float
    created_at: datetime
    current_ts: datetime
    holdings: List[HoldingResponse]
    daily_pnl: float
