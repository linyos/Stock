try:
    import certifi
    import os
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    print("[警告] 未安裝 certifi，相依套件憑證問題可能無法解決。請執行: python -m pip install certifi")

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from utils import *


def main():
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
    # for log in trade_log:
    #     print(log)
    # plot_results(df, buy_dates, buy_prices, sell_dates, sell_prices, ticker)


    # MACD分析
    df = calculateMacd(df)
    df, macd_buy_dates, macd_buy_prices, macd_sell_dates, macd_sell_prices = generate_macd_signals(df)
    #plot_results(df, macd_buy_dates, macd_buy_prices, macd_sell_dates, macd_sell_prices, ticker)
    plot_macd_results(df, macd_buy_dates, macd_buy_prices, macd_sell_dates, macd_sell_prices, ticker)






if __name__ == '__main__':
    main()