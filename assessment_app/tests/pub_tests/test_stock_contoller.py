import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "stocktester",
        "email": "stocktester@example.com",
        "password": "testpassword",
        "name": "Stock Tester"
    }

@pytest.fixture
def auth_token(test_user):
    client.post("/register", json=test_user)
    login_resp = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    return login_resp.cookies.get("access_token")

def test_create_stock(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    stock_data = {
        "symbol": "TSLA",
        "name": "Tesla Inc."
    }
    response = client.post("/stocks", json=stock_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "TSLA"
    assert data["name"] == "Tesla Inc."

def test_get_stocks(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.get("/stocks", headers=headers)
    assert response.status_code == 200
    stocks = response.json()
    assert isinstance(stocks, list)
    if stocks:
        assert "symbol" in stocks[0]
        assert "name" in stocks[0]
