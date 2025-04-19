# tests/utils.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assessment_app.repository.base import Base
from assessment_app.models.userinfo import UserInfo
from assessment_app.models.stock import Stock
from assessment_app.models.stock_price import StockPrice
from assessment_app.models.trade import Trade
from assessment_app.models.holding import Holding
from assessment_app.models.portfolio import Portfolio
from assessment_app.models.backTest import Backtest


def create_test_db():
    """Create an in-memory test database with all tables and return a session."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    return TestingSessionLocal()
