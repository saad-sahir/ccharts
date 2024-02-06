#%%

import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots
from skopt import gp_minimize
from skopt.space import Integer
import numpy as np


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

#%%


fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['AAPL.Open'], high=df['AAPL.High'],
                low=df['AAPL.Low'], close=df['AAPL.Close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False)
pio.show(fig, renderer="browser")

# %%
## INDICATORS

def calculate_ema(data, window=12):
    return data.ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd_line = short_ema - long_ema
    signal_line = calculate_ema(macd_line, signal_window)
    macd_histogram = macd_line - signal_line
    return macd_line, signal_line, macd_histogram

def plot_candlestick_with_indicators(df, show_rsi=True, show_macd=True, ema_windows=[]):
    if len(ema_windows) > 3:
        print("Maximum of 3 EMAs allowed. Plotting with the first 3 EMAs provided.")
        ema_windows = ema_windows[:3]

    # Create subplots
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        row_heights=[0.6, 0.2, 0.2])

    # Add Candlestick chart to main plot
    fig.add_trace(go.Candlestick(x=df['Date'],
                    open=df['AAPL.Open'], high=df['AAPL.High'],
                    low=df['AAPL.Low'], close=df['AAPL.Close'],
                    increasing_line_color='cyan', decreasing_line_color='gray'), row=1, col=1)

    # Add selected indicators
    row_rsi = 2 if (show_rsi or show_macd) else 1
    row_macd = 3 if show_macd else 1

    if show_rsi:
        fig.add_trace(go.Scatter(x=df['Date'], y=calculate_rsi(df['AAPL.Close']),
                                 mode='lines', name='RSI'), row=row_rsi, col=1)

    if show_macd:
        macd, signal, histogram = calculate_macd(df['AAPL.Close'])
        fig.add_trace(go.Scatter(x=df['Date'], y=macd, mode='lines', name='MACD'), row=row_macd, col=1)
        fig.add_trace(go.Scatter(x=df['Date'], y=signal, mode='lines', name='Signal'), row=row_macd, col=1)
        fig.add_trace(go.Bar(x=df['Date'], y=histogram, name='MACD Histogram'), row=row_macd, col=1)

    for idx, window in enumerate(ema_windows):
        ema = calculate_ema(df['AAPL.Close'], window=window)
        fig.add_trace(go.Scatter(x=df['Date'], y=ema, mode='lines', name=f'EMA {window}'), row=1, col=1)

    # Define layout
    fig.update_layout(xaxis_rangeslider_visible=False, title='AAPL Candlestick Chart with Indicators')
    fig.update_yaxes(title_text="Price", row=1, col=1)
    if show_rsi:
        fig.update_yaxes(title_text="RSI", row=row_rsi, col=1)
    if show_macd:
        fig.update_yaxes(title_text="MACD", row=row_macd, col=1)
    for idx, window in enumerate(ema_windows):
        fig.update_yaxes(title_text=f"EMA {window}", row=1, col=1)

    # Show the figure
    pio.show(fig, renderer="browser")

# Assuming df is already defined
ema1 = 20
ema2 = 50

plot_candlestick_with_indicators(df, show_rsi=True, show_macd=False, ema_windows=[ema1,ema2])

#%%
## CORSS-OVER STRATEGY OPTIMIZATION

def crossover_strategy_performance(df, ema_short_window, ema_long_window, initial_cash):
    # Calculate EMAs
     ema_short = calculate_ema(df['AAPL.Close'], window=ema_short_window)
     ema_long = calculate_ema(df['AAPL.Close'], window=ema_long_window)
     
     # Initialize variables
     cash = initial_cash
     shares = 0
     last_signal = 0  # 1 if last signal was to buy, -1 if last signal was to sell

     # Simulate trading
     for i in range(1, len(df)):
          if ema_short.iloc[i] > ema_long.iloc[i] and ema_short.iloc[i-1] <= ema_long.iloc[i-1]:
               # Buy signal
               shares_to_buy = cash / df['AAPL.Close'].iloc[i]
               shares += shares_to_buy
               cash = 0
               last_signal = 1
          elif ema_short.iloc[i] < ema_long.iloc[i] and ema_short.iloc[i-1] >= ema_long.iloc[i-1]:
               # Sell signal
               cash += shares * df['AAPL.Close'].iloc[i]
               shares = 0
               last_signal = -1
     
     # Final value
     final_value = cash + shares * df['AAPL.Close'].iloc[-1]
     if last_signal == 1:
          last_signal = "BUY"
     else:
          last_signal = "SELL"
     # Return final value and last signal
     return final_value, last_signal

final_cash, last_signal = crossover_strategy_performance(df, 20, 50, 10000)
print("THE FINAL CASH IS: ", final_cash)
print("THE LAST SIGNAL IS: ", last_signal)

# %%
def find_best_ema_parameters(df, initial_cash=10000, ema_short_range=(5, 200), ema_long_range=(10, 200)):
    best_final_value = -float('inf')
    best_ema_short = None
    best_ema_long = None

    for ema_short_window in range(ema_short_range[0], ema_short_range[1] + 1):
        for ema_long_window in range(ema_long_range[0], ema_long_range[1] + 1):
            final_value, _ = crossover_strategy_performance(df, ema_short_window, ema_long_window, initial_cash)
            if final_value > best_final_value:
                best_final_value = final_value
                best_ema_short = ema_short_window
                best_ema_long = ema_long_window

    return best_ema_short, best_ema_long

best_ema_short, best_ema_long = find_best_ema_parameters(df)
print("Best EMA Short Window:", best_ema_short)
print("Best EMA Long Window:", best_ema_long)

final_cash, last_signal = crossover_strategy_performance(df, best_ema_short, best_ema_long, 10000)
print("THE FINAL CASH IS: ", final_cash)
print("THE LAST SIGNAL IS: ", last_signal)
# %%
