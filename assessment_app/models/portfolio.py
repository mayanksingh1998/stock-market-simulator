# assessment_app/models/portfolio.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from assessment_app.repository.base import Base


class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("user_info.id"), nullable=False)
    name = Column(String, nullable=False)
    cash = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    current_ts = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserInfo", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="portfolio", cascade="all, delete-orphan")
