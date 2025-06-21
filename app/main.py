from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.stock_routes import router as stock_router

# 建立 FastAPI 應用程式
app = FastAPI(
    title="Stock Backtest API",
    description="股票回測後端服務，提供 MA 與 MACD 策略回測及圖表生成",
    version="1.0.0"
)

# 設定 CORS（方便前端或 Line Bot 呼叫）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 註冊路由
app.include_router(stock_router, prefix="/api/v1")

# 根路徑
@app.get("/")
async def root():
    return {
        "message": "Stock Backtest API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/v1/backtest/ma": "回測 MA 策略",
            "POST /api/v1/backtest/macd": "回測 MACD 策略",
            "GET /api/v1/plot/ma": "取得 MA 策略圖表",
            "GET /api/v1/plot/macd": "取得 MACD 策略圖表"
        }
    }

# 健康檢查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
