from pydantic import BaseModel
from assessment_app.models.constants import StockSymbols

class StockCreate(BaseModel):
    symbol: StockSymbols
    name: str

class StockResponse(BaseModel):
    id: int
    symbol: StockSymbols
    name: str

    class Config:
        orm_mode = True
