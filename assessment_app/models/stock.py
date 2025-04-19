from sqlalchemy import Column, Integer, String, DateTime, Enum as PgEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from assessment_app.models.constants import StockSymbols
from assessment_app.repository.base import Base


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(PgEnum(StockSymbols, name="stock_symbols_enum"), unique=True, nullable=False)
    name = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    trades = relationship("Trade", back_populates="stock")
    prices = relationship("StockPrice", back_populates="stock")  # <-- Add this line

