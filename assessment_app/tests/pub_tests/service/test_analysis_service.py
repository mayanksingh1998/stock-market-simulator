import pytest
from datetime import datetime
from fastapi import HTTPException


from assessment_app.models.stock import Stock
from assessment_app.models.stock_price import StockPrice
from assessment_app.models.portfolio import Portfolio
from assessment_app.models.holding import Holding
from assessment_app.service.analysis_service import get_stock_cagr_return, get_portfolio_cagr_return


def test_get_stock_cagr_return_success(mocker):
    db = mocker.Mock()

    stock = Stock(id=1, symbol="AAPL")
    db.query().filter().first.side_effect = [
        stock,  # Stock lookup
        StockPrice(stock_id=1, date=datetime(2023, 1, 1).date(), open=100.0),  # Start price
        StockPrice(stock_id=1, date=datetime(2024, 1, 1).date(), close=150.0)  # End price
    ]

    start_ts = datetime(2023, 1, 1)
    end_ts = datetime(2024, 1, 1)

    cagr = get_stock_cagr_return("HDFCBANK", start_ts, end_ts, db)
    expected_cagr = (150.0 / 100.0) ** (1 / 1) - 1
    assert round(cagr, 6) == round(expected_cagr, 6)


def test_get_stock_cagr_return_stock_not_found(mocker):
    db = mocker.Mock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_stock_cagr_return("INVALID", datetime(2023, 1, 1), datetime(2024, 1, 1), db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Stock not found"


def test_get_stock_cagr_return_missing_prices(mocker):
    db = mocker.Mock()

    stock = Stock(id=1, symbol="HDFCBANK")
    db.query().filter().first.side_effect = [
        stock,
        None,  # Start price missing
        StockPrice(stock_id=1, date=datetime(2024, 1, 1).date(), close=150.0)
    ]

    with pytest.raises(HTTPException) as exc_info:
        get_stock_cagr_return("HDFCBANK", datetime(2023, 1, 1), datetime(2024, 1, 1), db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Stock prices not available for given timestamps"


def test_get_portfolio_cagr_return_success(mocker):
    db = mocker.Mock()

    portfolio = Portfolio(id=1, user_id=1)
    holding = Holding(portfolio_id=1, stock_id=1, quantity=10)

    db.query().filter().all.side_effect = [
        [portfolio],  # Portfolios
        [holding]     # Holdings
    ]

    db.query().filter().order_by().first.side_effect = [
        StockPrice(stock_id=1, date=datetime(2023, 1, 1), open=100.0),  # Start price
        StockPrice(stock_id=1, date=datetime(2024, 1, 1), close=150.0)  # End price
    ]

    start_ts = datetime(2023, 1, 1)
    end_ts = datetime(2024, 1, 1)

    cagr = get_portfolio_cagr_return(1, start_ts, end_ts, db)
    expected_cagr = (1500 / 1000) ** (1 / 1) - 1
    assert round(cagr, 6) == round(expected_cagr, 6)


def test_get_portfolio_cagr_return_zero_start_value(mocker):
    db = mocker.Mock()

    portfolio = Portfolio(id=1, user_id=1)
    holding = Holding(portfolio_id=1, stock_id=1, quantity=10)

    db.query().filter().all.side_effect = [
        [portfolio],  # Portfolios
        [holding]     # Holdings
    ]

    db.query().filter().order_by().first.side_effect = [
        None,  # Start price is missing or zero
        StockPrice(stock_id=1, date=datetime(2024, 1, 1), close=150.0)
    ]

    with pytest.raises(HTTPException) as exc_info:
        get_portfolio_cagr_return(1, datetime(2023, 1, 1), datetime(2024, 1, 1), db)

    assert exc_info.value.status_code == 400
    assert "Start portfolio value is zero" in exc_info.value.detail


def test_get_portfolio_cagr_user_has_no_portfolios(mocker):
    db = mocker.Mock()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        get_portfolio_cagr_return(99, datetime(2023, 1, 1), datetime(2024, 1, 1), db)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User has no portfolios"
