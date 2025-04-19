from assessment_app.repository.base import Base
from assessment_app.repository.database import engine, SessionLocal
from assessment_app.models.userinfo import UserInfo
from assessment_app.models.stock import Stock
from assessment_app.models.stock_price import StockPrice
from assessment_app.models.trade import Trade
from assessment_app.models.backTest import Backtest
from assessment_app.models.holding import Holding
from assessment_app.models.portfolio import Portfolio



Base.metadata.create_all(bind=engine)
print("✅ Tables created.")

def seed_stocks():
    session = SessionLocal()

    stocks_to_seed = [
        {"symbol": "HDFCBANK", "name": "HDFC Bank"},
        {"symbol": "ICICIBANK", "name": "ICICI Bank"},
        {"symbol": "RELIANCE", "name": "Reliance Industries"},
        {"symbol": "TATAMOTORS", "name": "Tata Motors"},
    ]

    existing_symbols = {s.symbol for s in session.query(Stock).all()}

    new_stocks = [
        Stock(symbol=stock["symbol"], name=stock["name"])
        for stock in stocks_to_seed
        if stock["symbol"] not in existing_symbols
    ]

    if new_stocks:
        session.add_all(new_stocks)
        session.commit()
        print(f"✅ Inserted {len(new_stocks)} new stock(s): {[s.symbol for s in new_stocks]}")
    else:
        print("ℹ️ Stocks already seeded.")

    session.close()

seed_stocks()
