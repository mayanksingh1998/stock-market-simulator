import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)


@pytest.fixture
def test_user():
    return {
        "username": "backtester",
        "email": "backtester@example.com",
        "password": "backtestpass",
        "name": "Back Test"
    }


@pytest.fixture
def auth_token(test_user):
    client.post("/register", json=test_user)
    response = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    return response.cookies.get("access_token")


@pytest.fixture
def backtest_payload():
    return {
        "strategy": "buy_and_hold",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "initial_cash": 10000.0,
        "stock_ids": [1]  # Make sure the stock with ID 1 exists or mock accordingly
    }


def test_backtest_strategy(auth_token, backtest_payload):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.post("/backtest", json=backtest_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert "final_value" in data
    assert "returns" in data
    assert "pnl_over_time" in data
    assert isinstance(data["pnl_over_time"], list)
