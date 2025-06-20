import os
import sys
import base64
import io
from typing import Tuple, List
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 設定非互動模式後端

# 加入父目錄到路徑，以便匯入 utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import *
from app.models.schemas import BacktestResponse, TradeRecord, PlotResponse


class StockService:
    """股票服務類別"""
    
    def __init__(self):
        self.static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static')
        if not os.path.exists(self.static_dir):
            os.makedirs(self.static_dir)
    
    def backtest_ma_strategy(self, ticker: str, start: str, end: str) -> BacktestResponse:
        """回測 MA 策略"""
        try:
            csv_path = f'{ticker.lower()}_stock_data.csv'
            download_data(ticker, start, end, csv_path)
            df = load_data(csv_path)
            df = calculate_ma(df)
            df, buy_dates, buy_prices, sell_dates, sell_prices = generate_signals(df)
            total_return, trade_log = backtest(df, buy_dates, buy_prices, sell_dates, sell_prices)
            
            # 轉換交易紀錄格式
            formatted_trade_log = []
            for record in trade_log:
                formatted_trade_log.append(TradeRecord(
                    date=record[0].strftime('%Y-%m-%d'),
                    action=record[1],
                    price=record[2]
                ))
            
            return BacktestResponse(
                ticker=ticker,
                start=start,
                end=end,
                total_return=round(total_return, 2),
                trade_log=formatted_trade_log
            )
        except Exception as e:
            raise Exception(f"MA策略回測失敗: {str(e)}")
    
    def backtest_macd_strategy(self, ticker: str, start: str, end: str) -> BacktestResponse:
        """回測 MACD 策略"""
        try:
            csv_path = f'{ticker.lower()}_stock_data.csv'
            download_data(ticker, start, end, csv_path)
            df = load_data(csv_path)
            df = calculateMacd(df)
            df, buy_dates, buy_prices, sell_dates, sell_prices = generate_macd_signals(df)
            total_return, trade_log = backtest(df, buy_dates, buy_prices, sell_dates, sell_prices)
            
            # 轉換交易紀錄格式
            formatted_trade_log = []
            for record in trade_log:
                formatted_trade_log.append(TradeRecord(
                    date=record[0].strftime('%Y-%m-%d'),
                    action=record[1],
                    price=record[2]
                ))
            
            return BacktestResponse(
                ticker=ticker,
                start=start,
                end=end,
                total_return=round(total_return, 2),
                trade_log=formatted_trade_log
            )
        except Exception as e:
            raise Exception(f"MACD策略回測失敗: {str(e)}")
    
    def generate_ma_plot(self, ticker: str, start: str, end: str) -> PlotResponse:
        """產生 MA 策略圖表"""
        try:
            csv_path = f'{ticker.lower()}_stock_data.csv'
            download_data(ticker, start, end, csv_path)
            df = load_data(csv_path)
            df = calculate_ma(df)
            df, buy_dates, buy_prices, sell_dates, sell_prices = generate_signals(df)
            
            # 生成圖表
            plt.figure(figsize=(14, 7))
            plt.plot(df.index, df['Close'], label=f'{ticker} Close')
            plt.plot(df.index, df['MA20'], label='MA20')
            plt.plot(df.index, df['MA60'], label='MA60')
            plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
            plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
            plt.legend()
            plt.title(f'{ticker} Moving Average Strategy Backtest')
            plt.tight_layout()
            
            # 轉換為 base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return PlotResponse(
                ticker=ticker,
                image_base64=image_base64
            )
        except Exception as e:
            raise Exception(f"MA圖表生成失敗: {str(e)}")
    
    def generate_macd_plot(self, ticker: str, start: str, end: str) -> PlotResponse:
        """產生 MACD 策略圖表"""
        try:
            csv_path = f'{ticker.lower()}_stock_data.csv'
            download_data(ticker, start, end, csv_path)
            df = load_data(csv_path)
            df = calculateMacd(df)
            df, buy_dates, buy_prices, sell_dates, sell_prices = generate_macd_signals(df)
            
            # 生成圖表
            plt.figure(figsize=(14, 7))
            plt.plot(df.index, df['Close'], label=f'{ticker} Close')
            plt.plot(df.index, df['MACD'], label='MACD', color='blue')
            plt.plot(df.index, df['Signal_Line'], label='Signal Line', color='orange')
            plt.bar(df.index, df['Hist'], label='Histogram', color='gray', alpha=0.5)
            plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100, zorder=5)
            plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100, zorder=5)
            plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
            plt.legend()
            plt.title(f'{ticker} MACD Strategy Backtest')
            plt.tight_layout()
            
            # 轉換為 base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return PlotResponse(
                ticker=ticker,
                image_base64=image_base64
            )
        except Exception as e:
            raise Exception(f"MACD圖表生成失敗: {str(e)}")
