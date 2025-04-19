import pytest
from datetime import date
from sqlalchemy.orm import Session

from assessment_app.models import Portfolio, Stock, StockPrice, Holding
from assessment_app.schemas.portfolio import PortfolioRequest
from assessment_app.service import portfolio_service


@pytest.fixture
def sample_stock(db: Session):
    stock = Stock(symbol="TEST", name="Test Stock")
    db.add(stock)
    db.commit()
    return stock


def test_create_portfolio(db: Session, test_user):
    req = PortfolioRequest(name="My Portfolio", initial_funds=10000)
    portfolio = portfolio_service.create_portfolio(db, test_user.id, req)
    assert portfolio.name == "My Portfolio"
    assert portfolio.cash == 10000
    assert portfolio.user_id == test_user.id


def test_get_user_portfolios(db: Session, test_user, sample_stock):
    # Create a portfolio and holding
    portfolio = portfolio_service.create_portfolio(
        db, test_user.id, PortfolioRequest(name="Test Portfolio", initial_funds=10000)
    )

    holding = Holding(portfolio_id=portfolio.id, stock_id=sample_stock.id, quantity=10, avg_buy_price=100)
    db.add(holding)

    db.add(StockPrice(stock_id=sample_stock.id, date=date.today(), open=100, close=110))
    db.commit()

    portfolios = portfolio_service.get_user_portfolios(db, test_user.id)
    assert len(portfolios) >= 1
    assert isinstance(portfolios[0].daily_pnl, float)


def test_get_portfolio_by_id(db: Session, test_user, sample_stock):
    portfolio = portfolio_service.create_portfolio(
        db, test_user.id, PortfolioRequest(name="Growth", initial_funds=5000)
    )
    holding = Holding(portfolio_id=portfolio.id, stock_id=sample_stock.id, quantity=5, avg_buy_price=100)
    db.add(holding)
    db.add(StockPrice(stock_id=sample_stock.id, date=date.today(), close=120))
    db.commit()

    result = portfolio_service.get_portfolio_by_id(db, portfolio.id, test_user.id)
    assert "portfolio" in result
    assert "holdings" in result
    assert result["daily_pnl"] > 0


def test_get_holdings(db: Session, test_user, sample_stock):
    portfolio = portfolio_service.create_portfolio(
        db, test_user.id, PortfolioRequest(name="Income", initial_funds=2000)
    )
    holding = Holding(portfolio_id=portfolio.id, stock_id=sample_stock.id, quantity=3, avg_buy_price=50)
    db.add(holding)
    db.add(StockPrice(stock_id=sample_stock.id, date=date.today(), close=70))
    db.commit()

    holdings = portfolio_service.get_holdings(db, portfolio.id)
    assert len(holdings) > 0
    assert holdings[0].pnl == round((70 - 50) * 3, 2)
