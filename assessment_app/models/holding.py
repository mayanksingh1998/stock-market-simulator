# assessment_app/models/holding.py

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from assessment_app.repository.base import Base


class Holding(Base):
    __tablename__ = "holding"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, ForeignKey("portfolio.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    avg_buy_price = Column(Float, nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")
