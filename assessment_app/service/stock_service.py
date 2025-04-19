from sqlalchemy.orm import Session
from fastapi import HTTPException

from assessment_app.models.stock import Stock
from assessment_app.models.userinfo import UserInfo
from assessment_app.schemas.stock import StockCreate


def create_stock_logic(db: Session, stock: StockCreate, current_user: UserInfo) -> Stock:
    db_stock = db.query(Stock).filter(Stock.symbol == stock.symbol).first()
    if db_stock:
        raise HTTPException(status_code=400, detail="Stock with this symbol already exists.")

    new_stock = Stock(symbol=stock.symbol, name=stock.name)
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock


def get_stocks_logic(db: Session, current_user: UserInfo):
    return db.query(Stock).all()
