try:
    import certifi
    import os
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    print("[警告] 未安裝 certifi，相依套件憑證問題可能無法解決。請執行: python -m pip install certifi")

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# 取得特斯拉歷史股價資料
# df = yf.download("TSLA", start="2020-01-01", end="2025-01-01")
# print(df.head())
# 存成csv檔案
#df.to_csv('tsla_stock_data.csv')



csv_path = 'tsla_stock_data.csv'


# 判斷是否已經有資料檔案，若沒有則下載
if not os.path.exists('tsla_stock_data.csv'):
    df = yf.download("TSLA", start="2020-01-01", end="2025-01-01")
    df.to_csv('tsla_stock_data.csv')

#讀取tsla_stock_data.csv
#df = pd.read_csv('tsla_stock_data.csv', index_col='Date', parse_dates=True)

col_names =  ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
df = pd.read_csv(
    csv_path, 
    skiprows=2,           # 跳過前兩行
    names=col_names,     # 指定列名
    index_col='Date',     # 用 Date 當索引
    parse_dates=True      # 自動解析日期
)
# 檢查資料是否正確
# print(df.head())
# print(df.columns)

# 計算短期（20日）與長期（60日）移動平均線
df['MA20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['MA60'] = df['Close'].ewm(span=60, adjust=False).mean()


# 當短期均線上穿長期均線時買進，下穿時賣出

df['Signal'] = 0
# 判斷 20 日均線（MA20）是否大於 60 日均線（MA60）
df['Signal'][20:] = (df['MA20'][20:] > df['MA60'][20:]).astype(int)
df['Position'] = df['Signal'].diff()

#5. 回測交易策略
initial_cash = 100000  # 初始資金
cash = initial_cash
hold = 0
trade_log = []


buy_dates = []
buy_prices = []
sell_dates = []
sell_prices = []
for i in range(1, len(df)):
    if df['Position'].iloc[i] == 1:  # 買進訊號
        hold = cash / df['Close'].iloc[i]
        cash = 0
        trade_log.append((df.index[i], 'Buy', df['Close'].iloc[i]))
        buy_dates.append(df.index[i])
        buy_prices.append(df['Close'].iloc[i])
    elif df['Position'].iloc[i] == -1 and hold > 0:  # 賣出訊號
        cash = hold * df['Close'].iloc[i]
        hold = 0
        trade_log.append((df.index[i], 'Sell', df['Close'].iloc[i]))
        sell_dates.append(df.index[i])
        sell_prices.append(df['Close'].iloc[i])

# 若最後還持有股票，按最後一天收盤價賣出
if hold > 0:
    cash = hold * df['Close'].iloc[-1]
    trade_log.append((df.index[-1], 'Sell', df['Close'].iloc[-1]))
    sell_dates.append(df.index[-1])
    sell_prices.append(df['Close'].iloc[-1])

total_return = (cash - initial_cash) / initial_cash * 100
print(f"總報酬率：{total_return:.2f}%")
print("交易紀錄：")
# for log in trade_log:
#     print(log)

# 檢查買進點，確認 MA20 > MA60
for date in buy_dates:
    print(f" 檢查買進點 {date}: MA20={df.loc[date, 'MA20']}, MA60={df.loc[date, 'MA60']}, 收盤價={df.loc[date, 'Close']}")
    
# 檢查賣出點，確認 MA20 < MA60
for date in sell_dates:
    print(f"檢查賣出點 {date}: MA20={df.loc[date, 'MA20']}, MA60={df.loc[date, 'MA60']}, 收盤價={df.loc[date, 'Close']}")

# 6. 可視化績效
# 若繪圖資料點太多，可考慮重新取樣（例如：每5個資料點取一個）
#df_plot = df.iloc[::5]  # 每5個資料點取一個
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['Close'], label='TSLA Close')
plt.plot(df.index, df['MA20'], label='MA20')
plt.plot(df.index, df['MA60'], label='MA60')

# 標記買進點（綠色向上三角形）
plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
# 標記賣出點（紅色向下三角形）
plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)

# plt.xticks(rotation=45) 
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))  # 限制x軸顯示的刻度數量



plt.legend()
plt.title('TSLA Moving Average Strategy Backtest')
plt.tight_layout()
plt.show()