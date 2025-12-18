"""
Monthly Aggregation Module
Handles resampling daily data to monthly frequency with proper OHLC logic.
"""
import pandas as pd
from typing import Dict


def aggregate_monthly_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resample daily data to monthly frequency with proper OHLC aggregation.
    
    Monthly Aggregation Logic:
    - Open: First trading day's open price of the month
    - Close: Last trading day's close price of the month
    - High: Maximum high price during the month
    - Low: Minimum low price during the month
    - Volume: Sum of volumes during the month
    - AdjClose: Last trading day's adjusted close price of the month
    
    Args:
        df: DataFrame with date as index, containing daily OHLC data
        
    Returns:
        DataFrame with monthly aggregated data
    """
    # Group by ticker and resample to monthly frequency
    # Use 'ME' (Month End) instead of deprecated 'M'
    monthly_data = df.groupby('ticker').resample('ME').agg({
        'open': 'first',      # First trading day's open
        'high': 'max',        # Maximum high during month
        'low': 'min',         # Minimum low during month
        'close': 'last',      # Last trading day's close
        'adjclose': 'last',   # Last trading day's adjusted close
        'volume': 'sum'       # Sum of volumes
    })
    
    # Reset index - ticker is already in the index, date becomes a column
    monthly_data = monthly_data.reset_index()
    
    # Set date as index again for easier processing
    monthly_data = monthly_data.set_index('date')
    
    # Remove rows with missing data (shouldn't happen, but safety check)
    monthly_data = monthly_data.dropna(subset=['open', 'high', 'low', 'close'])
    
    return monthly_data


def get_monthly_data_by_ticker(monthly_df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Extract monthly data for a specific ticker.
    
    Args:
        monthly_df: DataFrame with monthly aggregated data
        ticker: Stock ticker symbol
        
    Returns:
        DataFrame filtered for the specific ticker, sorted by date
    """
    ticker_data = monthly_df[monthly_df['ticker'] == ticker].copy()
    ticker_data = ticker_data.sort_index()  # Sort by date
    return ticker_data

