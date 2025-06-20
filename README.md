# 股票回測 FastAPI 後端服務

此專案提供股票技術分析回測的 **FastAPI 後端服務**，支援 MA（移動平均）與 MACD 兩種策略，提供 RESTful API 介面，方便前後端分離架構與 Line Bot 串接。

## 專案架構

```
Stock/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 主應用程式
│   ├── api/
│   │   ├── __init__.py
│   │   └── stock_routes.py  # API 路由
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic 模型
│   └── services/
│       ├── __init__.py
│       └── stock_service.py # 業務邏輯
├── static/                  # 靜態檔案
├── run_server.py           # 伺服器啟動腳本
├── test_api.py             # API 測試範例
├── stock.py                # 原始腳本（保留作為備份）
├── utils.py                # 核心功能函式
└── requirements.txt        # 套件相依
```

## API 端點

- **POST** `/api/v1/backtest/ma` - 回測 MA 策略
- **POST** `/api/v1/backtest/macd` - 回測 MACD 策略  
- **GET** `/api/v1/plot/ma` - 取得 MA 策略圖表
- **GET** `/api/v1/plot/macd` - 取得 MACD 策略圖表

## 快速開始

### 1. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 2. 啟動 API 伺服器
```bash
python run_server.py
```

### 3. 查看 API 文件
瀏覽器開啟：http://localhost:8000/docs

### 4. 測試 API
```bash
python test_api.py
```

## API 使用範例

### 回測 MA 策略
```bash
curl -X POST "http://localhost:8000/api/v1/backtest/ma" \
     -H "Content-Type: application/json" \
     -d '{"ticker": "TSLA", "start": "2020-01-01", "end": "2025-01-01"}'
```

### 取得圖表
```bash
curl "http://localhost:8000/api/v1/plot/ma?ticker=TSLA&start=2020-01-01&end=2025-01-01"
```

## Line Bot 串接

此 API 設計適合 Line Bot 呼叫：
1. Line Bot 接收用戶輸入（股票代碼、期間） 
2. 透過 HTTP 請求呼叫本 API
3. 取得回測結果或圖表後回傳給用戶

## 注意事項
- 此回測範例僅供學習與研究，不代表任何投資建議
- 圖表以 base64 格式回傳，方便前端或 Bot 使用
- 支援 CORS，方便跨域呼叫

