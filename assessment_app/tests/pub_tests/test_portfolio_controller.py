import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "portfolio_tester",
        "email": "portfolio@example.com",
        "password": "testpassword",
        "name": "Portfolio Tester"
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
def create_portfolio(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    portfolio_data = {"name": "Test Portfolio", "cash": 10000.0}
    response = client.post("/portfolio", json=portfolio_data, headers=headers)
    return response.json()

def test_create_portfolio(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.post("/portfolio", json={"name": "New Portfolio", "cash": 5000.0}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Portfolio"
    assert data["cash"] == 5000.0

def test_get_user_portfolios(auth_token):
    headers = {"Cookie": f"access_token={auth_token}"}
    response = client.get("/portfolio", headers=headers)
    assert response.status_code == 200
    portfolios = response.json()
    assert isinstance(portfolios, list)
    if portfolios:
        assert "id" in portfolios[0]
        assert "name" in portfolios[0]

def test_get_portfolio_by_id(auth_token, create_portfolio):
    headers = {"Cookie": f"access_token={auth_token}"}
    portfolio_id = create_portfolio["id"]
    response = client.get(f"/portfolio/{portfolio_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == portfolio_id
    assert "cash" in data
    assert "holdings" in data

def test_get_portfolio_holdings(auth_token, create_portfolio):
    headers = {"Cookie": f"access_token={auth_token}"}
    portfolio_id = create_portfolio["id"]
    response = client.get(f"/portfolio/{portfolio_id}/holdings", headers=headers)
    assert response.status_code == 200
    holdings = response.json()
    assert isinstance(holdings, list)
