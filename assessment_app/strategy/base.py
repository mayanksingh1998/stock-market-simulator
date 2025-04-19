# assessment_app/strategy/base.py

from abc import ABC, abstractmethod
from datetime import date
from sqlalchemy.orm import Session
from assessment_app.models.portfolio import Portfolio

class BaseStrategy(ABC):
    def __init__(self, db: Session, portfolio: Portfolio, current_date: date):
        self.db = db
        self.portfolio = portfolio
        self.current_date = current_date

    @abstractmethod
    def run(self):
        """
        Run the strategy logic.
        """
        pass
