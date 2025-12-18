"""
Technical Indicators Module
Calculates SMA and EMA using vectorized pandas operations.
"""
import pandas as pd
import numpy as np


def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA) using vectorized pandas operations.
    
    Formula: Sum of closing prices (over 'N' periods) / Number of periods (N)
    
    Args:
        series: Series of closing prices
        window: Number of periods (e.g., 10 or 20)
        
    Returns:
        Series with SMA values
    """
    return series.rolling(window=window, min_periods=1).mean()


def calculate_ema(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA) using the correct formula.
    
    Formula:
    - Multiplier (alpha) = 2 / (Number of Periods + 1)
    - EMA = (Current Price - Previous EMA) * Multiplier + Previous EMA
    - First EMA uses SMA as the initial value (as per specification)
    
    Args:
        series: Series of closing prices
        window: Number of periods (e.g., 10 or 20)
        
    Returns:
        Series with EMA values
    """
    # Calculate multiplier (smoothing constant) as per specification
    # alpha = 2 / (N + 1)
    alpha = 2.0 / (window + 1.0)
    
    # Initialize EMA series
    ema = pd.Series(index=series.index, dtype=float)
    
    # Calculate SMA for first 'window' periods to use as initial EMA value
    sma_initial = series.rolling(window=window, min_periods=1).mean()
    
    # For periods before we have enough data for SMA, use the price itself
    # Once we have 'window' periods, use SMA as the starting point
    for i in range(len(series)):
        if i < window - 1:
            # Before we have enough periods, use price itself
            ema.iloc[i] = series.iloc[i]
        elif i == window - 1:
            # At the window-th period, use SMA as initial EMA
            ema.iloc[i] = sma_initial.iloc[i]
        else:
            # Apply EMA formula: EMA = (Price - Previous EMA) * alpha + Previous EMA
            prev_ema = ema.iloc[i - 1]
            current_price = series.iloc[i]
            ema.iloc[i] = (current_price - prev_ema) * alpha + prev_ema
    
    return ema


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SMA 10, SMA 20, EMA 10, and EMA 20 columns to the dataframe.
    
    These indicators are calculated based on monthly closing prices.
    
    Args:
        df: DataFrame with monthly data, must have 'close' column
        
    Returns:
        DataFrame with added technical indicator columns
    """
    df = df.copy()
    
    # Ensure data is sorted by date
    df = df.sort_index()
    
    # Calculate technical indicators based on closing prices
    df['SMA_10'] = calculate_sma(df['close'], window=10)
    df['SMA_20'] = calculate_sma(df['close'], window=20)
    df['EMA_10'] = calculate_ema(df['close'], window=10)
    df['EMA_20'] = calculate_ema(df['close'], window=20)
    
    return df

