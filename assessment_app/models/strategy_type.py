# assessment_app/models/strategy_type.py
from enum import Enum

class StrategyType(str, Enum):
    MOVING_AVERAGE_CROSSOVER = "MOVING_AVERAGE_CROSSOVER"
    BUY_AND_HOLD = "BUY_AND_HOLD"
