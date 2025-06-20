try:
    import certifi
    import os
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    print("[警告] 未安裝 certifi，相依套件憑證問題可能無法解決。請執行: python -m pip install certifi")

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
"""
原始股票回測腳本 (已重構為 FastAPI 後端服務)
此檔案保留作為測試和備份用途

新的 API 服務請使用：
- 啟動伺服器：python run_server.py
- API 文件：http://localhost:8000/docs
"""

from utils import *


def main():
    """原始測試函數 - 已移至 FastAPI 服務"""
    print("此腳本已重構為 FastAPI 後端服務！")
    print("請使用以下指令啟動 API 伺服器：")
    print("  python run_server.py")
    print("API 文件位於：http://localhost:8000/docs")
    print()
    
    # 保留原始功能作為測試
    ticker = 'TSLA'
    start, end = '2020-01-01', '2025-01-01'
    csv_path = f'{ticker.lower()}_stock_data.csv'
    download_data(ticker, start, end, csv_path)
    df = load_data(csv_path)
    df = calculate_ma(df)
    df, buy_dates, buy_prices, sell_dates, sell_prices = generate_signals(df)
    total_return, trade_log = backtest(df, buy_dates, buy_prices, sell_dates, sell_prices)
    print(f'總報酬率：{total_return:.2f}%')
    print('交易紀錄：')
    for log in trade_log:
        print(log)


if __name__ == "__main__":
    main()






if __name__ == '__main__':
    main()