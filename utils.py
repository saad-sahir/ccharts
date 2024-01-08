# utils.py

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import json
import time

# Function to get market data from yfinance
def get_chart(market, interval, now=datetime.now()):
    start = now - timedelta(days=29 if interval in ['1d', '1h', '15m', '5m'] else 364)
    df = yf.download(market, start=start, end=now, interval=interval).reset_index()
    if 'Datetime' in df.columns: df = df.rename(columns={"Datetime": "Date",})
    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df