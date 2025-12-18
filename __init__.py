"""
Stock Data Processor Package
Modular solution for processing daily stock data into monthly aggregates with technical indicators.
"""

from .data_loader import load_stock_data, validate_tickers
from .monthly_aggregator import aggregate_monthly_ohlc, get_monthly_data_by_ticker
from .technical_indicators import calculate_sma, calculate_ema, add_technical_indicators
from .file_writer import write_ticker_to_csv, partition_and_write_results

__all__ = [
    'load_stock_data',
    'validate_tickers',
    'aggregate_monthly_ohlc',
    'get_monthly_data_by_ticker',
    'calculate_sma',
    'calculate_ema',
    'add_technical_indicators',
    'write_ticker_to_csv',
    'partition_and_write_results',
]

