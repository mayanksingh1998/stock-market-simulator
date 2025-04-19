import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from assessment_app.service.trade_service import place_trade_logic, get_user_trades_logic
from assessment_app.models import Portfolio, Holding, Trade
from assessment_app.models.constants import TradeType
from assessment_app.schemas.trade import TradeCreate
from assessment_app.models.userinfo import UserInfo
from assessment_app.models.stock import Stock
from assessment_app.tests.pub_tests.utils import create_test_db


@pytest.fixture
def db():
    db = create_test_db()
    yield db
    db.close()


@pytest.fixture
def test_user(db: Session):
    user = UserInfo(email="testuser@example.com", hashed_password="hashed", name="Test")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_stock(db: Session):
    stock = Stock(symbol="TCS", name="Tata Consultancy Services")
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@pytest.fixture
def test_portfolio(db: Session, test_user: UserInfo):
    portfolio = Portfolio(user_id=test_user.id, name="Main", cash=10000)
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


def test_place_buy_trade(db: Session, test_user: UserInfo, test_stock: Stock, test_portfolio: Portfolio):
    trade_data = TradeCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        trade_type=TradeType.BUY,
        quantity=10,
        price=100.0
    )

    trade = place_trade_logic(db, trade_data, test_user)

    assert trade.quantity == 10
    assert trade.price == 100.0
    holding = db.query(Holding).filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id).first()
    assert holding is not None
    assert holding.quantity == 10
    assert holding.avg_buy_price == 100.0


def test_place_sell_trade(db: Session, test_user: UserInfo, test_stock: Stock, test_portfolio: Portfolio):
    # First Buy
    buy = TradeCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        trade_type=TradeType.BUY,
        quantity=10,
        price=100.0
    )
    place_trade_logic(db, buy, test_user)

    # Then Sell
    sell = TradeCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        trade_type=TradeType.SELL,
        quantity=5,
        price=120.0
    )
    trade = place_trade_logic(db, sell, test_user)

    holding = db.query(Holding).filter_by(portfolio_id=test_portfolio.id, stock_id=test_stock.id).first()
    assert holding.quantity == 5
    assert test_portfolio.cash > 0


def test_sell_with_insufficient_holdings(db: Session, test_user: UserInfo, test_stock: Stock, test_portfolio: Portfolio):
    with pytest.raises(HTTPException) as e:
        sell = TradeCreate(
            portfolio_id=test_portfolio.id,
            stock_id=test_stock.id,
            trade_type=TradeType.SELL,
            quantity=5,
            price=100.0
        )
        place_trade_logic(db, sell, test_user)
    assert e.value.status_code == 400


def test_get_user_trades_logic(db: Session, test_user: UserInfo, test_stock: Stock, test_portfolio: Portfolio):
    trade = TradeCreate(
        portfolio_id=test_portfolio.id,
        stock_id=test_stock.id,
        trade_type=TradeType.BUY,
        quantity=1,
        price=50.0
    )
    place_trade_logic(db, trade, test_user)

    trades = get_user_trades_logic(db, test_user)
    assert len(trades) == 1
    assert trades[0].user_id == test_user.id
