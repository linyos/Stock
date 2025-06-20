"""
API 測試腳本範例
此腳本示範如何呼叫 FastAPI 後端服務進行回測
"""
import requests
import json

# API 基本設定
BASE_URL = "http://localhost:8000/api/v1"

def test_ma_backtest():
    """測試 MA 策略回測"""
    url = f"{BASE_URL}/backtest/ma"
    data = {
        "ticker": "TSLA",
        "start": "2020-01-01",
        "end": "2025-01-01"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("MA 策略回測結果:")
            print(f"股票代碼: {result['ticker']}")
            print(f"期間: {result['start']} - {result['end']}")
            print(f"總報酬率: {result['total_return']}%")
            print(f"交易次數: {len(result['trade_log'])}")
        else:
            print(f"請求失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"連線錯誤: {e}")

def test_macd_backtest():
    """測試 MACD 策略回測"""
    url = f"{BASE_URL}/backtest/macd"
    data = {
        "ticker": "TSLA",
        "start": "2020-01-01",
        "end": "2025-01-01"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("MACD 策略回測結果:")
            print(f"股票代碼: {result['ticker']}")
            print(f"期間: {result['start']} - {result['end']}")
            print(f"總報酬率: {result['total_return']}%")
            print(f"交易次數: {len(result['trade_log'])}")
        else:
            print(f"請求失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"連線錯誤: {e}")

def test_ma_plot():
    """測試 MA 策略圖表"""
    url = f"{BASE_URL}/plot/ma"
    params = {
        "ticker": "TSLA",
        "start": "2020-01-01",
        "end": "2025-01-01"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            print("MA 策略圖表已生成")
            print(f"股票代碼: {result['ticker']}")
            print(f"圖表格式: base64 (長度: {len(result['image_base64'])})")
        else:
            print(f"請求失敗: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"連線錯誤: {e}")

if __name__ == "__main__":
    print("=== API 測試 ===")
    print("請先啟動 FastAPI 伺服器: python run_server.py")
    print()
    
    test_ma_backtest()
    print()
    test_macd_backtest()
    print()
    test_ma_plot()
