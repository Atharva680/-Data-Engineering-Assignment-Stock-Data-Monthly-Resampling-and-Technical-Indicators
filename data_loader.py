"""
Data Loading Module
Handles reading and preprocessing of the input CSV file.
"""
import pandas as pd
from pathlib import Path
from typing import Optional


def load_stock_data(file_path: str) -> pd.DataFrame:
    """
    Load stock data from CSV file and prepare it for processing.
    
    Args:
        file_path: Path to the input CSV file
        
    Returns:
        DataFrame with date as index and properly typed columns
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If required columns are missing
    """
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    # Read CSV with date parsing
    df = pd.read_csv(
        file_path,
        parse_dates=['date']
    )
    
    # Ensure date is datetime type (parse_dates handles this, but double-check)
    df['date'] = pd.to_datetime(df['date'])
    
    # Validate required columns
    required_columns = ['date', 'volume', 'open', 'high', 'low', 'close', 'adjclose', 'ticker']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Ensure date is datetime type
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by ticker and date for proper resampling
    df = df.sort_values(['ticker', 'date']).reset_index(drop=True)
    
    # Set date as index for resampling operations
    df = df.set_index('date')
    
    return df


def validate_tickers(df: pd.DataFrame, expected_tickers: list) -> bool:
    """
    Validate that all expected tickers are present in the dataset.
    
    Args:
        df: DataFrame with stock data
        expected_tickers: List of expected ticker symbols
        
    Returns:
        True if all tickers are present
        
    Raises:
        ValueError: If any expected ticker is missing
    """
    unique_tickers = df['ticker'].unique().tolist()
    missing_tickers = [ticker for ticker in expected_tickers if ticker not in unique_tickers]
    
    if missing_tickers:
        raise ValueError(f"Missing expected tickers: {missing_tickers}")
    
    return True

