import string

from pydantic import BaseModel
from typing import Literal
from datetime import datetime

from assessment_app.models.constants import TradeType
from assessment_app.schemas.stock import StockResponse


class TradeCreate(BaseModel):
    stock_id: int
    trade_type: Literal[TradeType.BUY, TradeType.SELL]
    quantity: int
    price: float
    portfolio_id: str

class TradeResponse(BaseModel):
    id: int
    trade_type: TradeType
    quantity: int
    price: float
    timestamp: datetime
    stock: StockResponse  # include full stock info

    class Config:
        orm_mode = True
