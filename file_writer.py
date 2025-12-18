"""
File Writing Module
Handles partitioning and writing results to separate CSV files.
"""
import pandas as pd
from pathlib import Path
from typing import List


def write_ticker_to_csv(df: pd.DataFrame, ticker: str, output_dir: str = "output") -> str:
    """
    Write monthly aggregated data for a specific ticker to a CSV file.
    
    Args:
        df: DataFrame with monthly data for the ticker
        ticker: Stock ticker symbol
        output_dir: Directory to save output files
        
    Returns:
        Path to the created file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare dataframe for writing
    df_output = df.copy()
    
    # Reset index to have date as a column
    df_output = df_output.reset_index()
    
    # Select and order columns for output
    # Include: date, open, high, low, close, adjclose, volume, SMA_10, SMA_20, EMA_10, EMA_20
    output_columns = [
        'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume',
        'SMA_10', 'SMA_20', 'EMA_10', 'EMA_20'
    ]
    
    # Filter to only include columns that exist
    available_columns = [col for col in output_columns if col in df_output.columns]
    df_output = df_output[available_columns]
    
    # Generate filename
    filename = f"result_{ticker}.csv"
    file_path = output_path / filename
    
    # Write to CSV
    df_output.to_csv(file_path, index=False)
    
    return str(file_path)


def partition_and_write_results(
    monthly_df: pd.DataFrame,
    tickers: List[str],
    output_dir: str = "output"
) -> List[str]:
    """
    Partition monthly data by ticker and write to separate CSV files.
    
    Args:
        monthly_df: DataFrame with monthly aggregated data for all tickers
        tickers: List of ticker symbols to process
        output_dir: Directory to save output files
        
    Returns:
        List of file paths created
    """
    created_files = []
    
    for ticker in tickers:
        # Filter data for this ticker
        ticker_data = monthly_df[monthly_df['ticker'] == ticker].copy()
        
        if ticker_data.empty:
            print(f"Warning: No data found for ticker {ticker}")
            continue
        
        # Write to CSV
        file_path = write_ticker_to_csv(ticker_data, ticker, output_dir)
        created_files.append(file_path)
        
        # Verify row count (should be 24 months for 2-year period)
        row_count = len(ticker_data)
        print(f"Created {file_path} with {row_count} rows")
    
    return created_files

