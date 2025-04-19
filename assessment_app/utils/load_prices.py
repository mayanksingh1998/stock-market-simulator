# scripts/load_prices.py
import csv
from datetime import datetime

from assessment_app.models.constants import StockSymbols
from assessment_app.repository.database import SessionLocal
from assessment_app.models.stock import Stock
from assessment_app.models.stock_price import StockPrice

def load_csv_for_stock(symbol: str, file_path: str):
    session = SessionLocal()
    try:
        stock = session.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            print(f"❌ Stock symbol '{symbol}' not found.")
            return

        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            prices = []

            for row in reader:
                price = StockPrice(
                    stock_id=stock.id,
                    date=datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    adj_close=float(row["Adj Close"]),
                    volume=int(row["Volume"]),
                )
                prices.append(price)

            session.bulk_save_objects(prices)
            session.commit()
            print(f"✅ Loaded {len(prices)} prices for {symbol}")
    finally:
        session.close()

if __name__ == "__main__":
    files = {
        StockSymbols.HDFCBANK: "data/HDFCBANK.csv",
        StockSymbols.ICICIBANK: "data/ICICIBANK.csv",
        StockSymbols.RELIANCE: "data/RELIANCE.csv",
        StockSymbols.TATAMOTORS: "data/TATAMOTORS.csv"
    }

    for symbol, path in files.items():
        load_csv_for_stock(symbol, path)
