# assessment_app/models/trades.py
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from assessment_app.repository.base import Base

# In assessment_app/models/trade.py

class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"), nullable=False)
    portfolio_id = Column(String, ForeignKey("portfolio.id"), nullable=False)  # <-- ADD THIS
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    trade_type = Column(String, nullable=False)  # 'buy' or 'sell'
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserInfo", back_populates="trades")
    portfolio = relationship("Portfolio", back_populates="trades")  # <-- ADD THIS
    stock = relationship("Stock", back_populates="trades")
