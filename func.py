import pandas as pd
import numpy as np
from typing import Dict, Any


def calculate_moving_averages(df: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    df = df.copy()  
    df['short_ma'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['long_ma'] = df['close'].rolling(window=long_window, min_periods=1).mean()
    return df

def generate_signals(df: pd.DataFrame):

    df = df.copy()
    df['signal'] = 0  # Default: no action
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1   # Buy signal
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell signal
    #(Buy/Sell moments)
    #  1 for entering buy, -2 for switching from buy to sell
    df['positions'] = df['signal'].diff()
    
    return df



def calculate_performance(df: pd.DataFrame):
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']


    cumulative_return = (1 + df['strategy_returns']).prod() - 1
    total_trades = df['positions'].abs().sum() / 2 
    win_rate = (df['strategy_returns'] > 0).sum() / len(df.dropna())


    return { "cumulative_return": round(cumulative_return * 100, 2),
            "total_trades": int(total_trades),
            "win_rate": round(win_rate * 100, 2)}








