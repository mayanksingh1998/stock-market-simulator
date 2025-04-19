
# Stock Market Simulator

This is a FastAPI-based backend application simulating a stock market platform. It allows users to register, place trades, track their portfolio performance, and run strategy backtests.

## Features

- **User Management**: Register and login with JWT authentication.
- **Stock Management**: Create and view stocks.
- **Trade Execution**: Place buy/sell trades and manage holdings.
- **Portfolio Tracking**: Track cash, holdings, and daily P&L.
- **Strategy Backtesting**: Simulate trading strategies against historical data.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

To start the application:

```bash
./eval.sh
```
This will make you container up, also create the tables and seed the database with some initial data.

To stop the application:

```bash
./stop.sh
```

### Running Tests

To execute all test cases:

```bash
./execute_tests.sh
```

## API Endpoints

- `POST /register` – Register a new user
- `POST /login` – Login and get access token
- `GET /user` – Get current user info
- `POST /stocks` – Create a stock
- `GET /stocks` – Get all stocks
- `POST /trade` – Place a trade (buy/sell)
- `GET /trades` – Get trade history
- `POST /portfolio` – Create a new portfolio
- `GET /portfolio` – List user portfolios
- `GET /portfolio/{id}` – Get portfolio details
- `GET /portfolio/{id}/holdings` – View holdings in a portfolio
- `POST /backtest` – Run a strategy backtest
Currently we support two strategies:
  - `buy_and_hold`: Buy a stock and hold it for a specified period.
  - `moving_average`: Buy/sell based on moving average crossover strategy.
- `GET analysis/estimate_returns/portfolio?start_ts=2023-07-18T00:00:00&end_ts=2024-01-01T00:00:00`: To get analysis of any portfolio, but before that please do some trades  

- `GET analysis/estimate_returns/stock?stock_symbol=HDFCBANK&start_ts=2023-07-18T00:00:00&end_ts=2024-01-01T00:00:00`: To get analysis of any stock 

---

**Note**: All endpoints (except register/login) require authentication via JWT.
-----

You will get token in cookies of login api

📚 Docs
Interactive API docs available at:


Swagger: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc