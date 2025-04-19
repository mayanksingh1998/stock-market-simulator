# assessment_app/strategy/ma_crossover.py
from assessment_app.models.constants import TradeType
from assessment_app.strategy.base import BaseStrategy
from assessment_app.models.holding import Holding
from assessment_app.models.stock_price import StockPrice
from assessment_app.models.trade import Trade

from sqlalchemy.orm import Session
from datetime import date

SHORT_WINDOW = 5
LONG_WINDOW = 20

class MovingAverageCrossoverStrategy(BaseStrategy):
    def get_moving_average(self, prices, window):
        if len(prices) < window:
            return None
        return sum(p.close for p in prices[-window:]) / window

    def run(self):
        holdings = self.db.query(Holding).filter_by(portfolio_id=self.portfolio.id).all()

        for holding in holdings:
            prices = (
                self.db.query(StockPrice)
                .filter_by(stock_id=holding.stock_id)
                .filter(StockPrice.date <= self.current_date)
                .order_by(StockPrice.date.desc())
                .limit(LONG_WINDOW)
                .all()[::-1]  # reverse to get in ascending order again
            )

            if len(prices) < LONG_WINDOW:
                continue

            short_ma = self.get_moving_average(prices, SHORT_WINDOW)
            long_ma = self.get_moving_average(prices, LONG_WINDOW)
            last_price = prices[-1].close

            if not short_ma or not long_ma:
                continue

            if short_ma > long_ma and self.portfolio.cash >= last_price:
                print(f"Buying {holding.stock_id} at {last_price}")
                self.portfolio.cash -= last_price
                holding.quantity += 1
                self.db.add(Trade(
                    portfolio_id=self.portfolio.id,
                    stock_id=holding.stock_id,
                    trade_type=TradeType.BUY.value,
                    price=last_price,
                    quantity=1,
                    timestamp=self.current_date,
                    user_id = self.portfolio.user_id  # ✅ Set user_id

                ))
            elif short_ma < long_ma and holding.quantity > 0:
                print(f"Selling {holding.stock_id} at {last_price}")
                self.portfolio.cash += last_price
                holding.quantity -= 1
                self.db.add(Trade(
                    portfolio_id=self.portfolio.id,
                    stock_id=holding.stock_id,
                    trade_type=TradeType.SELL.value,
                    price=last_price,
                    quantity=1,
                    timestamp=self.current_date,
                    user_id=self.portfolio.user_id  # ✅ Set user_id

                ))

            self.db.add(holding)

        self.db.add(self.portfolio)

