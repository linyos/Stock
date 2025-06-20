from fastapi import APIRouter, HTTPException
from app.models.schemas import BacktestRequest, BacktestResponse, PlotRequest, PlotResponse
from app.services.stock_service import StockService

router = APIRouter()
stock_service = StockService()


@router.post("/backtest/ma", response_model=BacktestResponse)
async def backtest_ma_strategy(request: BacktestRequest):
    """回測 MA 策略"""
    try:
        return stock_service.backtest_ma_strategy(request.ticker, request.start, request.end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backtest/macd", response_model=BacktestResponse)
async def backtest_macd_strategy(request: BacktestRequest):
    """回測 MACD 策略"""
    try:
        return stock_service.backtest_macd_strategy(request.ticker, request.start, request.end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plot/ma", response_model=PlotResponse)
async def get_ma_plot(ticker: str = "TSLA", start: str = "2020-01-01", end: str = "2025-01-01"):
    """取得 MA 策略圖表"""
    try:
        return stock_service.generate_ma_plot(ticker, start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plot/macd", response_model=PlotResponse)
async def get_macd_plot(ticker: str = "TSLA", start: str = "2020-01-01", end: str = "2025-01-01"):
    """取得 MACD 策略圖表"""
    try:
        return stock_service.generate_macd_plot(ticker, start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
