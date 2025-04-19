from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from assessment_app.repository.base import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    trades = relationship("Trade", back_populates="user")
    backtests = relationship("Backtest", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")

