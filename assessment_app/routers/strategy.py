# import uuid
# from datetime import datetime
# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy import desc
# from sqlalchemy.orm import Session
#
# from assessment_app.models import StockPrice, Stock, Portfolio
# from assessment_app.models.holding import Holding
# from assessment_app.models.strategyExecution import StrategyExecution
# from assessment_app.models.strategy_type import StrategyType
# from assessment_app.repository import database
# from assessment_app.schemas.portfolio import PortfolioRequest, PortfolioResponse
#
# from assessment_app.service.auth_service import get_current_user
# from assessment_app.simulator.engine import execute_strategy
#
# # from assessment_app.models.models import Portfolio, PortfolioRequest, Strategy
# # from assessment_app.service.auth_service import get_current_user
# #
# router = APIRouter()
# #
# #
# # @router.get("/strategies", response_model=List[Strategy])
# # async def get_strategies(current_user_id: str = Depends(get_current_user)) -> List[Strategy]:
# #     """
# #     Get all strategies available. You do not need to implement this.
# #     """
# #     pass
# #
# #
# @router.post("/portfolio", response_model=PortfolioResponse)
# def create_portfolio(
#     portfolio_request: PortfolioRequest,
#     current_user_id: str = Depends(get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     portfolio = Portfolio(
#         id=str(uuid.uuid4()),
#         user_id=current_user_id,
#         name=portfolio_request.name,
#         cash=portfolio_request.initial_funds,
#         current_ts=portfolio_request.current_ts or datetime.utcnow(),
#     )
#     db.add(portfolio)
#     db.commit()
#     db.refresh(portfolio)
#     return portfolio
# #
# @router.get("/portfolio/{portfolio_id}", response_model=PortfolioResponse)
# def get_portfolio_by_id(
#     portfolio_id: str,
#     current_user_id: str = Depends(get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     portfolio = db.query(Portfolio).filter_by(id=portfolio_id, user_id=current_user_id).first()
#     if not portfolio:
#         raise HTTPException(status_code=404, detail="Portfolio not found")
#     return portfolio
#
#
# @router.delete("/portfolio/{portfolio_id}", response_model=PortfolioResponse)
# def delete_portfolio(
#     portfolio_id: str,
#     current_user_id: str = Depends(get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     portfolio = db.query(Portfolio).filter_by(id=portfolio_id, user_id=current_user_id).first()
#     if not portfolio:
#         raise HTTPException(status_code=404, detail="Portfolio not found")
#
#     db.delete(portfolio)
#     db.commit()
#     return portfolio
#
#
#
# @router.get("/portfolio-net-worth", response_model=float)
# def get_net_worth(
#     portfolio_id: str,
#     current_user_id: str = Depends(get_current_user),
#     db: Session = Depends(database.get_db),
# ):
#     portfolio = db.query(Portfolio).filter_by(id=portfolio_id, user_id=current_user_id).first()
#     if not portfolio:
#         raise HTTPException(status_code=404, detail="Portfolio not found")
#
#     total_net_worth = portfolio.cash
#
#     holdings = db.query(Holding).filter_by(portfolio_id=portfolio.id).all()
#
#     for holding in holdings:
#         stock = db.query(Stock).filter_by(symbol=holding.stock_symbol).first()
#         if not stock:
#             continue
#
#         latest_price = (
#             db.query(StockPrice)
#             .filter_by(stock_id=stock.id)
#             .order_by(desc(StockPrice.date))
#             .first()
#         )
#         if latest_price:
#             total_net_worth += holding.quantity * latest_price.close
#
#     return total_net_worth