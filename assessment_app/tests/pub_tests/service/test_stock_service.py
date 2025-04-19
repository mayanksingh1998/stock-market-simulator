import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from assessment_app.service.stock_service import create_stock_logic, get_stocks_logic
from assessment_app.models.stock import Stock
from assessment_app.schemas.stock import StockCreate
from assessment_app.models.userinfo import UserInfo


@pytest.fixture
def mock_db_session(mocker):
    return mocker.MagicMock(spec=Session)


@pytest.fixture
def dummy_user():
    return UserInfo(id=1, username="testuser")


def test_create_stock_success(mock_db_session, dummy_user):
    stock_data = StockCreate(symbol="HDFCBANK", name="HDFC Bank Ltd")

    # Simulate no stock with that symbol already exists
    mock_db_session.query().filter().first.return_value = None

    # Simulate DB commit and refresh behavior
    mock_db_session.add.side_effect = lambda obj: setattr(obj, "id", 1)

    result = create_stock_logic(mock_db_session, stock_data, dummy_user)

    assert result.symbol == "HDFCBANK"
    assert result.name == "HDFC Bank Ltd"
    mock_db_session.add.assert_called_once()


def test_create_stock_duplicate(mock_db_session, dummy_user):
    stock_data = StockCreate(symbol="HDFCBANK", name="HDFC Bank Ltd")

    # Simulate stock already exists
    mock_db_session.query().filter().first.return_value = Stock(symbol="HDFCBANK", name="HDFC Bank Ltd")

    with pytest.raises(HTTPException) as exc_info:
        create_stock_logic(mock_db_session, stock_data, dummy_user)

    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


def test_get_stocks(mock_db_session, dummy_user):
    mock_stocks = [
        Stock(symbol="HDFCBANK", name="HDFC Bank Ltd"),
        Stock(symbol="ICICIBANK", name="ICICI Bank Ltd"),
    ]

    mock_db_session.query().all.return_value = mock_stocks

    result = get_stocks_logic(mock_db_session, dummy_user)

    assert len(result) == 2
    assert result[0].symbol == "HDFCBANK"
    assert result[1].symbol == "ICICIBANK"
