# Stock Data Processor - Data Engineering Assignment

## Overview

This project processes daily stock price data into monthly aggregates with technical indicators. It transforms a 2-year historical dataset containing daily stock prices for 10 unique symbols into monthly summaries with calculated technical indicators.

## Features

- **Monthly Resampling**: Converts daily data to monthly frequency with proper OHLC aggregation
- **Technical Indicators**: Calculates SMA 10, SMA 20, EMA 10, and EMA 20
- **Data Partitioning**: Generates separate CSV files for each stock symbol
- **Modular Architecture**: Clean separation of concerns with dedicated modules

## Project Structure

```
stock_data_processor/
├── __init__.py                 # Package initialization
├── data_loader.py              # Data loading and validation
├── monthly_aggregator.py       # Monthly OHLC aggregation logic
├── technical_indicators.py     # SMA and EMA calculations
└── file_writer.py             # File partitioning and writing

process_stock_data.py          # Main execution script
README_STOCK_PROCESSOR.md      # This file
```

## Requirements

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.20.0

## Installation

```bash
pip install pandas numpy
```

## Usage

### Basic Usage

```bash
python process_stock_data.py <input_file.csv> [output_dir]
```

**Example:**
```bash
python process_stock_data.py data/stock_data.csv output
```

### Input File Format

The input CSV must contain the following columns:
- `date`: Date in YYYY-MM-DD format
- `volume`: Trading volume
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `adjclose`: Adjusted closing price
- `ticker`: Stock ticker symbol (AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA)

### Output

The script generates 10 CSV files in the output directory (default: `output/`):
- `result_AAPL.csv`
- `result_AMD.csv`
- `result_AMZN.csv`
- `result_AVGO.csv`
- `result_CSCO.csv`
- `result_MSFT.csv`
- `result_NFLX.csv`
- `result_PEP.csv`
- `result_TMUS.csv`
- `result_TSLA.csv`

Each file contains exactly 24 rows (one for each month in the 2-year period) with the following columns:
- `date`: Month end date
- `open`: First trading day's open price of the month
- `high`: Maximum high price during the month
- `low`: Minimum low price during the month
- `close`: Last trading day's close price of the month
- `adjclose`: Last trading day's adjusted close price
- `volume`: Sum of volumes during the month
- `SMA_10`: 10-period Simple Moving Average
- `SMA_20`: 20-period Simple Moving Average
- `EMA_10`: 10-period Exponential Moving Average
- `EMA_20`: 20-period Exponential Moving Average

## Monthly Aggregation Logic

- **Open**: The price at the first trading day of the month
- **Close**: The price at the last trading day of the month
- **High**: The maximum price reached during the month
- **Low**: The minimum price reached during the month
- **Volume**: Sum of all trading volumes during the month

## Technical Indicators

### Simple Moving Average (SMA)

Formula: `SMA = Sum of closing prices (over N periods) / N`

- **SMA_10**: 10-period simple moving average
- **SMA_20**: 20-period simple moving average

### Exponential Moving Average (EMA)

Formula:
- Multiplier = 2 / (N + 1)
- EMA = (Current Price - Previous EMA) × Multiplier + Previous EMA
- First EMA uses SMA as the initial value

- **EMA_10**: 10-period exponential moving average
- **EMA_20**: 20-period exponential moving average

## Implementation Details

### Vectorization

All calculations use vectorized pandas operations for optimal performance:
- `rolling().mean()` for SMA calculations
- `ewm(span=N, adjust=False)` for EMA calculations
- `groupby().resample()` for monthly aggregation

### Code Structure

The solution is modular with clear separation of concerns:

1. **Data Loading** (`data_loader.py`): Handles CSV reading, validation, and preprocessing
2. **Monthly Aggregation** (`monthly_aggregator.py`): Implements OHLC resampling logic
3. **Technical Indicators** (`technical_indicators.py`): Calculates SMA and EMA using vectorized operations
4. **File Writing** (`file_writer.py`): Partitions data and writes to separate CSV files

## Assumptions

1. **Data Completeness**: The dataset contains complete daily data for all 10 tickers across the 2-year period. Missing trading days are handled by pandas resampling.

2. **Date Range**: The dataset covers exactly 24 months (2 years). The script will process all available months, but expects 24 months per ticker.

3. **Trading Days**: The script assumes standard trading days (Monday-Friday, excluding holidays). Non-trading days are automatically handled during monthly resampling.

4. **Data Quality**: The input CSV is assumed to be clean with no duplicate dates per ticker. If duplicates exist, the last occurrence is used.

5. **Monthly Boundaries**: Monthly resampling uses calendar month boundaries. The "first trading day" refers to the first available trading day within each calendar month.

6. **EMA Initialization**: For the first EMA value, we use the first available closing price (effectively SMA with window=1). This ensures EMA values are available from the start.

7. **Output Directory**: The output directory is created automatically if it doesn't exist.

## Dataset

The dataset can be downloaded from:
https://github.com/sandeep-tt/tt-intern-dataset

After downloading, place the CSV file in your project directory or provide the path when running the script.

## Example Output

```
============================================================
Stock Data Processor - Monthly Aggregation & Technical Indicators
============================================================

[Step 1] Loading data from: stock_data.csv
✓ Loaded 5040 daily records

[Step 2] Validating tickers...
✓ All 10 expected tickers found

[Step 3] Resampling to monthly frequency...
✓ Created 240 monthly records

[Step 4] Calculating technical indicators...
✓ Added SMA 10, SMA 20, EMA 10, and EMA 20 indicators

[Step 5] Partitioning and writing results to output/...
Created output/result_AAPL.csv with 24 rows
Created output/result_AMD.csv with 24 rows
...
✓ Successfully created 10 output files

============================================================
Processing Summary
============================================================
  result_AAPL.csv: 24 rows
  result_AMD.csv: 24 rows
  ...
============================================================

✓ Processing complete!
```

## Testing

To verify the output:
1. Check that 10 files are created
2. Verify each file has exactly 24 rows
3. Validate that SMA_10 and SMA_20 are calculated correctly (compare with manual calculation)
4. Validate that EMA_10 and EMA_20 follow the exponential smoothing formula

## Notes

- The script uses pandas' built-in functions for all calculations, avoiding third-party technical analysis libraries as required.
- All operations are vectorized for optimal performance.
- The code is designed to be readable and maintainable with clear function names and documentation.

## License

This project is created for educational purposes as part of a data engineering assignment.

