import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from fastapi import status

from assessment_app.main import app
from assessment_app.models import UserInfo


# Mocking the dependencies
@pytest.fixture(autouse=True)
def override_dependencies(mocker):
    # Mock get_db to return a dummy Session
    mock_db = mocker.Mock()
    app.dependency_overrides = {}

    # Return user with id=1 for auth
    mock_user = UserInfo(id=1, email="user@example.com", username="testuser")
    app.dependency_overrides = {
        # Auth
        "assessment_app.service.auth_service.get_current_user": lambda: mock_user,
        # DB
        "assessment_app.repository.database.get_db": lambda: mock_db
    }

    yield
    app.dependency_overrides = {}  # clean up


client = TestClient(app)


def test_get_stock_analysis_success(mocker):
    mock_return_value = 0.15
    mock_func = mocker.patch(
        "assessment_app.service.analysis_service.get_stock_cagr_return",
        return_value=mock_return_value
    )

    response = client.get(
        "/analysis/estimate_returns/stock",
        params={
            "stock_symbol": "AAPL",
            "start_ts": "2023-01-01T00:00:00",
            "end_ts": "2024-01-01T00:00:00"
        }
    )

    assert response.status_code == 200
    assert response.json() == mock_return_value
    mock_func.assert_called_once()


def test_estimate_portfolio_returns_success(mocker):
    mock_return_value = 0.12
    mock_func = mocker.patch(
        "assessment_app.service.analysis_service.get_portfolio_cagr_return",
        return_value=mock_return_value
    )

    response = client.get(
        "/analysis/estimate_returns/portfolio",
        params={
            "start_ts": "2023-01-01T00:00:00",
            "end_ts": "2024-01-01T00:00:00"
        }
    )

    assert response.status_code == 200
    assert response.json() == mock_return_value
    mock_func.assert_called_once_with(1, datetime(2023, 1, 1), datetime(2024, 1, 1), mocker.ANY)


def test_get_stock_analysis_not_found(mocker):
    mocker.patch(
        "assessment_app.service.analysis_service.get_stock_cagr_return",
        side_effect=Exception("Stock not found")
    )

    response = client.get(
        "/analysis/estimate_returns/stock",
        params={
            "stock_symbol": "INVALID",
            "start_ts": "2023-01-01T00:00:00",
            "end_ts": "2024-01-01T00:00:00"
        }
    )

    assert response.status_code == 500  # Since it's a generic Exception
    assert "Stock not found" in response.text


def test_estimate_portfolio_returns_zero_start_value(mocker):
    from fastapi import HTTPException

    mocker.patch(
        "assessment_app.service.analysis_service.get_portfolio_cagr_return",
        side_effect=HTTPException(status_code=400, detail="Start portfolio value is zero")
    )

    response = client.get(
        "/analysis/estimate_returns/portfolio",
        params={
            "start_ts": "2023-01-01T00:00:00",
            "end_ts": "2024-01-01T00:00:00"
        }
    )

    assert response.status_code == 400
    assert "Start portfolio value is zero" in response.text
