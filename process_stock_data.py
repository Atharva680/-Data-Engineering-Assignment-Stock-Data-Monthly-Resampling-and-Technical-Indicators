"""
Main Script: Stock Data Processor
Processes daily stock data into monthly aggregates with technical indicators.

This script:
1. Loads daily stock data from CSV
2. Resamples to monthly frequency with proper OHLC aggregation
3. Calculates SMA 10, SMA 20, EMA 10, and EMA 20
4. Partitions results into separate CSV files (one per ticker)
"""
import sys
import pandas as pd
from pathlib import Path

from stock_data_processor import (
    load_stock_data,
    validate_tickers,
    aggregate_monthly_ohlc,
    add_technical_indicators,
    partition_and_write_results
)


# Expected tickers in the dataset
EXPECTED_TICKERS = ['AAPL', 'AMD', 'AMZN', 'AVGO', 'CSCO', 'MSFT', 'NFLX', 'PEP', 'TMUS', 'TSLA']


def main(input_file: str, output_dir: str = "output"):
    """
    Main processing function.
    
    Args:
        input_file: Path to input CSV file with daily stock data
        output_dir: Directory to save output CSV files
    """
    print("=" * 60)
    print("Stock Data Processor - Monthly Aggregation & Technical Indicators")
    print("=" * 60)
    
    # Step 1: Load data
    print(f"\n[Step 1] Loading data from: {input_file}")
    try:
        df_daily = load_stock_data(input_file)
        print(f"[OK] Loaded {len(df_daily)} daily records")
    except Exception as e:
        print(f"[ERROR] Error loading data: {e}")
        sys.exit(1)
    
    # Step 2: Validate tickers
    print(f"\n[Step 2] Validating tickers...")
    try:
        validate_tickers(df_daily, EXPECTED_TICKERS)
        print(f"[OK] All {len(EXPECTED_TICKERS)} expected tickers found")
    except Exception as e:
        print(f"[ERROR] Error validating tickers: {e}")
        sys.exit(1)
    
    # Step 3: Aggregate to monthly frequency
    print(f"\n[Step 3] Resampling to monthly frequency...")
    try:
        df_monthly = aggregate_monthly_ohlc(df_daily)
        print(f"[OK] Created {len(df_monthly)} monthly records")
    except Exception as e:
        print(f"[ERROR] Error aggregating data: {e}")
        sys.exit(1)
    
    # Step 4: Calculate technical indicators
    print(f"\n[Step 4] Calculating technical indicators...")
    try:
        # Group by ticker and calculate indicators for each
        monthly_with_indicators = []
        
        for ticker in EXPECTED_TICKERS:
            ticker_data = df_monthly[df_monthly['ticker'] == ticker].copy()
            
            if not ticker_data.empty:
                ticker_data = add_technical_indicators(ticker_data)
                monthly_with_indicators.append(ticker_data)
        
        df_monthly_final = pd.concat(monthly_with_indicators, ignore_index=False)
        print(f"[OK] Added SMA 10, SMA 20, EMA 10, and EMA 20 indicators")
    except Exception as e:
        print(f"[ERROR] Error calculating indicators: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 5: Partition and write results
    print(f"\n[Step 5] Partitioning and writing results to {output_dir}/...")
    try:
        created_files = partition_and_write_results(
            df_monthly_final,
            EXPECTED_TICKERS,
            output_dir
        )
        print(f"\n[OK] Successfully created {len(created_files)} output files")
        
        # Summary
        print("\n" + "=" * 60)
        print("Processing Summary")
        print("=" * 60)
        for file_path in sorted(created_files):
            df_check = pd.read_csv(file_path)
            print(f"  {Path(file_path).name}: {len(df_check)} rows")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] Error writing files: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n[OK] Processing complete!")


if __name__ == "__main__":
    
    # Default input file (can be overridden via command line)
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Try to find the dataset file
        possible_paths = [
            "data/stock_data.csv",
            "stock_data.csv",
            "dataset.csv",
            "data.csv"
        ]
        
        input_file = None
        for path in possible_paths:
            if Path(path).exists():
                input_file = path
                break
        
        if not input_file:
            print("Error: Input file not found.")
            print("Usage: python process_stock_data.py <input_file.csv> [output_dir]")
            print("\nPlease provide the path to your stock data CSV file.")
            sys.exit(1)
    
    # Optional output directory
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    main(input_file, output_dir)

