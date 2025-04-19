# buy_and_hold.py
from assessment_app.strategy.base import BaseStrategy
from assessment_app.models.holding import Holding
from assessment_app.models.trade import Trade
from assessment_app.models.constants import TradeType
from assessment_app.models.stock_price import StockPrice

class BuyAndHoldStrategy(BaseStrategy):
    def run(self):
        for holding in self.portfolio.holdings:
            latest_price = (
                self.db.query(StockPrice)
                .filter_by(stock_id=holding.stock_id)
                .filter(StockPrice.date <= self.current_date)
                .order_by(StockPrice.date.desc())
                .first()
            )
            if not latest_price:
                continue

            if holding.quantity == 0 and self.portfolio.cash >= latest_price.close:
                holding.quantity += 1
                self.portfolio.cash -= latest_price.close

                self.db.add(Trade(
                    portfolio_id=self.portfolio.id,
                    stock_id=holding.stock_id,
                    trade_type=TradeType.BUY.value,
                    price=latest_price.close,
                    quantity=1,
                    timestamp=self.current_date
                ))

            self.db.add(holding)
        self.db.add(self.portfolio)
