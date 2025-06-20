from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BacktestRequest(BaseModel):
    """回測請求模型"""
    ticker: str = "TSLA"
    start: str = "2020-01-01"
    end: str = "2025-01-01"


class TradeRecord(BaseModel):
    """交易紀錄模型"""
    date: str
    action: str  # "Buy" or "Sell"
    price: float


class BacktestResponse(BaseModel):
    """回測回應模型"""
    ticker: str
    start: str
    end: str
    total_return: float
    trade_log: List[TradeRecord]


class PlotRequest(BaseModel):
    """圖表請求模型"""
    ticker: str = "TSLA"
    start: str = "2020-01-01"
    end: str = "2025-01-01"


class PlotResponse(BaseModel):
    """圖表回應模型"""
    ticker: str
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
