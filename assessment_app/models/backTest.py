from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from assessment_app.repository.base import Base


class Backtest(Base):
    __tablename__ = "backtest"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user_info.id"), nullable=False)
    user = relationship("UserInfo", back_populates="backtests")

    strategy_name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    initial_balance = Column(Float, nullable=False)
    final_balance = Column(Float, nullable=True)
    returns = Column(Float, nullable=True)

    trade_log = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
