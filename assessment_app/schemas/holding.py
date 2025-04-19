# assessment_app/schemas/holding.py
from typing import Optional

from pydantic import BaseModel
from uuid import UUID

class HoldingResponse(BaseModel):
    id: UUID
    portfolio_id: UUID
    stock_id: int
    quantity: int
    avg_buy_price: float
    daily_pnl: Optional[float] = None


    class Config:
        orm_mode = True
