# 股票移動平均策略回測

此專案提供一個簡單範例，示範如何使用 Python 針對特斯拉（TSLA）股票進行移動平均交叉策略的回測。腳本會下載或讀取 `tsla_stock_data.csv`，計算 20 日與 60 日指數移動平均線，並以交叉點作為買賣時機，同時繪出股價與買賣點圖表。

## 主要檔案
- `stock.py`：主要程式碼，包含資料下載、策略計算與圖形化結果。
- `tsla_stock_data.csv`：預先下載的歷史股價資料，若檔案不存在，程式會透過 [yfinance](https://github.com/ranaroussi/yfinance) 下載資料並建立檔案。

## 執行方式
1. 安裝相依套件：
   ```bash
   pip install pandas matplotlib yfinance certifi
   ```
2. 執行程式：
   ```bash
   python stock.py
   ```
程式會輸出交易紀錄與總報酬率，並繪製移動平均線與交易點位圖表。

## 注意事項
- 此回測範例僅供學習與研究，不代表任何投資建議。
- 若執行環境無法顯示視覺化圖表，可考慮將 `matplotlib` 的後端改為 `Agg`。

