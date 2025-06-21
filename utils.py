import os
import yfinance as yf
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def download_data(ticker, start, end, csv_path):
    """下載資料至csv，若已存在則跳過。"""
    if not os.path.exists(csv_path):
        df = yf.download(ticker, start=start, end=end)
        if df is not None and not df.empty:
            df.to_csv(csv_path)
        else:
            df = None
    else:
        df = None
    return df


def load_data(csv_path):
    """讀取csv資料成DataFrame。"""
    col_names = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df = pd.read_csv(
        csv_path,
        skiprows=2,
        names=col_names,
        index_col='Date',
        parse_dates=True
    )
    return df


def calculate_ma(df, span_short=20, span_long=60):
    """計算短期與長期指數移動平均。"""
    df['MA20'] = df['Close'].ewm(span=span_short, adjust=False).mean()
    df['MA60'] = df['Close'].ewm(span=span_long, adjust=False).mean()
    return df


def calculateMacd(df, short_window=12, long_window=26, signal_window=9):
    """計算MACD指標。訊號線、柱狀圖"""
    df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['Hist'] = df['MACD'] - df['Signal_Line']
    return df


def generate_signals(df):
    """產生交易訊號與買賣點列表。"""
    df['Signal'] = 0
    df.loc[df.index[20:], 'Signal'] = (df['MA20'][20:] > df['MA60'][20:]).astype(int)
    df['Position'] = df['Signal'].diff()
    buy_dates, buy_prices, sell_dates, sell_prices = [], [], [], []
    for i in range(1, len(df)):
        if df['Position'].iloc[i] == 1:
            buy_dates.append(df.index[i])
            buy_prices.append(df['Close'].iloc[i])
        elif df['Position'].iloc[i] == -1:
            sell_dates.append(df.index[i])
            sell_prices.append(df['Close'].iloc[i])
    # 若最後仍持有，於最後日賣出
    if df['Position'].iloc[-1] == 1:
        sell_dates.append(df.index[-1])
        sell_prices.append(df['Close'].iloc[-1])
    return df, buy_dates, buy_prices, sell_dates, sell_prices


def backtest(df, buy_dates, buy_prices, sell_dates, sell_prices, initial_cash=100000):
    """回測策略，回傳總報酬與交易紀錄。"""
    cash, hold = initial_cash, 0
    trade_log = []
    # 逐筆執行買賣
    for date, price in zip(buy_dates, buy_prices):
        hold = cash / price
        cash = 0
        trade_log.append((date, 'Buy', price))
    for date, price in zip(sell_dates, sell_prices):
        cash = hold * price
        hold = 0
        trade_log.append((date, 'Sell', price))
    total_return = (cash - initial_cash) / initial_cash * 100
    return total_return, trade_log


# 4. 產生交叉訊號
#   當 MACD 線上穿訊號線 => 買進 (1)；下穿 => 賣出 (-1)
def generate_macd_signals(df):
    """產生MACD交易訊號與買賣點列表。"""
    df['Signal'] = 0
    df.loc[df.index[26:], 'Signal'] = (df['MACD'][26:] > df['Signal_Line'][26:]).astype(int)
    df['Position'] = df['Signal'].diff()
    buy_dates, buy_prices, sell_dates, sell_prices = [], [], [], []
    for i in range(1, len(df)):
        if df['Position'].iloc[i] == 1:
            buy_dates.append(df.index[i])
            buy_prices.append(df['Close'].iloc[i])
        elif df['Position'].iloc[i] == -1:
            sell_dates.append(df.index[i])
            sell_prices.append(df['Close'].iloc[i])
    # 若最後仍持有，於最後日賣出
    if df['Position'].iloc[-1] == 1:
        sell_dates.append(df.index[-1])
        sell_prices.append(df['Close'].iloc[-1])
    return df, buy_dates, buy_prices, sell_dates, sell_prices


def plot_results(df, buy_dates, buy_prices, sell_dates, sell_prices, ticker):
    """繪製回測結果圖表。"""
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label=f'{ticker} Close')
    plt.plot(df.index, df['MA20'], label='MA20')
    plt.plot(df.index, df['MA60'], label='MA60')
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
    plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)
    plt.gca().xaxis.set_major_locator(MaxNLocator(10))
    plt.legend()
    plt.title(f'{ticker} Moving Average Strategy Backtest')
    plt.tight_layout()
    plt.show()


def plot_macd_results(df, buy_dates, buy_prices, sell_dates, sell_prices, ticker):
    """繪製MACD回測結果圖表。"""
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label=f'{ticker} Close')
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['Signal_Line'], label='Signal Line', color='orange')
    plt.bar(df.index, df['Hist'], label='Histogram', color='gray', alpha=0.5)
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
    plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)
    plt.gca().xaxis.set_major_locator(MaxNLocator(10))
    plt.legend()
    plt.title(f'{ticker} MACD Strategy Backtest')
    plt.tight_layout()
    plt.show()
