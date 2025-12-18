"""
Test script to verify the stock data processor functionality.
This script can be used to test the processor with sample data or validate outputs.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

from stock_data_processor import (
    load_stock_data,
    aggregate_monthly_ohlc,
    add_technical_indicators,
    calculate_sma,
    calculate_ema
)


def create_sample_data(output_file: str = "sample_stock_data.csv"):
    """
    Create a sample dataset for testing purposes.
    Generates 2 years of daily data for all 10 tickers.
    """
    tickers = ['AAPL', 'AMD', 'AMZN', 'AVGO', 'CSCO', 'MSFT', 'NFLX', 'PEP', 'TMUS', 'TSLA']
    
    # Generate 2 years of trading days (approximately 252 trading days per year)
    start_date = datetime(2022, 1, 1)
    dates = []
    current_date = start_date
    
    # Generate approximately 504 trading days (2 years)
    while len(dates) < 504:
        # Skip weekends
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current_date)
        current_date += timedelta(days=1)
        if len(dates) >= 504:
            break
    
    # Create sample data
    data = []
    np.random.seed(42)  # For reproducibility
    
    for ticker in tickers:
        base_price = np.random.uniform(50, 500)
        
        for date in dates:
            # Generate realistic price movements
            change = np.random.uniform(-0.05, 0.05)
            base_price = base_price * (1 + change)
            
            open_price = base_price
            high_price = base_price * (1 + np.random.uniform(0, 0.03))
            low_price = base_price * (1 - np.random.uniform(0, 0.03))
            close_price = base_price * (1 + np.random.uniform(-0.02, 0.02))
            adjclose = close_price * np.random.uniform(0.98, 1.02)
            volume = int(np.random.uniform(1000000, 10000000))
            
            data.append({
                'date': date,
                'ticker': ticker,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'adjclose': round(adjclose, 2),
                'volume': volume
            })
    
    df = pd.DataFrame(data)
    df = df.sort_values(['ticker', 'date'])
    df.to_csv(output_file, index=False)
    print(f"Created sample dataset: {output_file} with {len(df)} rows")
    return output_file


def test_sma_calculation():
    """Test SMA calculation with known values."""
    print("\n[Test] SMA Calculation")
    print("-" * 40)
    
    # Create simple test data
    test_prices = pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    sma_5 = calculate_sma(test_prices, window=5)
    
    # Manual calculation: (10+20+30+40+50)/5 = 30
    expected_first_sma = 30.0
    
    print(f"Test prices: {test_prices.tolist()}")
    print(f"SMA(5) values: {sma_5.tolist()}")
    print(f"First SMA(5) value: {sma_5.iloc[4]:.2f} (expected: {expected_first_sma:.2f})")
    
    assert abs(sma_5.iloc[4] - expected_first_sma) < 0.01, "SMA calculation incorrect"
    print("[PASS] SMA calculation test passed")


def test_ema_calculation():
    """Test EMA calculation."""
    print("\n[Test] EMA Calculation")
    print("-" * 40)
    
    # Create simple test data
    test_prices = pd.Series([10, 20, 30, 40, 50])
    ema_3 = calculate_ema(test_prices, window=3)
    
    print(f"Test prices: {test_prices.tolist()}")
    print(f"EMA(3) values: {[f'{x:.2f}' for x in ema_3.tolist()]}")
    
    # Verify EMA is calculated (should be different from SMA)
    sma_3 = calculate_sma(test_prices, window=3)
    print(f"SMA(3) values: {[f'{x:.2f}' for x in sma_3.tolist()]}")
    
    # EMA should be different from SMA (except possibly first value)
    assert not ema_3.equals(sma_3), "EMA should differ from SMA"
    print("[PASS] EMA calculation test passed")


def test_monthly_aggregation():
    """Test monthly aggregation logic."""
    print("\n[Test] Monthly Aggregation")
    print("-" * 40)
    
    # Create sample data for one ticker
    dates = pd.date_range('2022-01-01', '2022-01-31', freq='D')
    dates = [d for d in dates if d.weekday() < 5]  # Only weekdays
    
    test_data = pd.DataFrame({
        'date': dates,
        'ticker': 'TEST',
        'open': range(100, 100 + len(dates)),
        'high': range(105, 105 + len(dates)),
        'low': range(95, 95 + len(dates)),
        'close': range(102, 102 + len(dates)),
        'adjclose': range(102, 102 + len(dates)),
        'volume': [1000000] * len(dates)
    })
    test_data = test_data.set_index('date')
    
    monthly = aggregate_monthly_ohlc(test_data)
    
    print(f"Daily records: {len(test_data)}")
    print(f"Monthly records: {len(monthly)}")
    print(f"First month open: {monthly.iloc[0]['open']} (should be first day's open)")
    print(f"First month close: {monthly.iloc[0]['close']} (should be last day's close)")
    
    assert len(monthly) == 1, "Should have 1 monthly record for January"
    assert monthly.iloc[0]['open'] == 100, "Open should be first day's open"
    print("[PASS] Monthly aggregation test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Stock Data Processor - Test Suite")
    print("=" * 60)
    
    # Run tests
    test_sma_calculation()
    test_ema_calculation()
    test_monthly_aggregation()
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    
    # Automatically create sample data
    print("\nCreating sample dataset for testing...")
    sample_file = create_sample_data()
    print(f"\nSample dataset created: {sample_file}")
    print("You can now run: python process_stock_data.py sample_stock_data.csv")

