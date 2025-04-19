from assessment_app.routers import stocks, trades, portfolio, backtest, analysis
from assessment_app.routers.user_mgmt import router as user_mgmt_router

import logging
from fastapi import FastAPI

from assessment_app.repository import database  # This runs Base.metadata.create_all()

app = FastAPI()

app.include_router(user_mgmt_router, prefix="", tags=["user_mgmt"])
app.include_router(stocks.router, prefix="", tags=["stocks"])
app.include_router(trades.router, prefix="", tags=["trades"])
app.include_router(portfolio.router, prefix="", tags=["portfolio"])
app.include_router(backtest.router, prefix="", tags=["backtest"])
app.include_router(analysis.router, prefix="", tags=["analysis"])



@app.get("/")
def root():
    return {"message": "FastAPI up and running!"}