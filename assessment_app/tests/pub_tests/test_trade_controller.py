import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "tradeuser",
        "email": "tradeuser@example.com",
        "password": "testpassword",
        "name": "Trade Tester"
    }

@pytest.fixture
def auth_token(test_user):
    # Register
    client.post("/register", json=test_user)
    # Login
    login_resp = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    return login_resp.cookies.get("access_token")

@pytest.fixture
def test_portfolio(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.post("/portfolio", json={"name": "Test Portfolio", "initial_funds": 10000}, headers=headers)
    return response.json()["id"]

@pytest.fixture
def test_stock(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    stock_data = {"symbol": "AAPL", "name": "Apple Inc."}
    response = client.post("/stocks", json=stock_data, headers=headers)
    return response.json()["id"]

def test_place_trade(auth_token, test_portfolio, test_stock):
    headers = {"Cookie": f"access_token={auth_token}"}
    trade_data = {
        "stock_id": test_stock,
        "portfolio_id": test_portfolio,
        "trade_type": "BUY",
        "quantity": 10,
        "price": 100.0
    }
    response = client.post("/trade", json=trade_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["stock_id"] == test_stock
    assert data["trade_type"] == "BUY"
    assert data["quantity"] == 10
    assert data["price"] == 100.0

def test_get_user_trades(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.get("/trades", headers=headers)
    assert response.status_code == 200
    trades = response.json()
    assert isinstance(trades, list)
    # optionally assert specific keys or values in trades[0] if expected
