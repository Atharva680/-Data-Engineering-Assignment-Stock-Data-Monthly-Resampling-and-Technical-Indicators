# -Data-Engineering-Assignment-Stock-Data-Monthly-Resampling-and-Technical-Indicators
## 1. Overview

The script processes two years of daily stock price data for 10 selected tickers. Key operations include:

1. **Resampling** data from daily to monthly frequency.  
2. Computing monthly **aggregates** (Open, High, Low, Close — OHLC).  
3. Calculating **technical indicators** such as SMA(10), SMA(20), EMA(10), and EMA(20).  
4. **Partitioning** the processed results into separate CSV files for each ticker.

***

## 2. Dataset Information

- **Source:** [GitHub Repository](https://github.com/sandeep-tt/tt-intern-dataset)  
- **File:** `output_file.csv`  
- **Tickers:** AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA  
- **Date Range:** 2018-01-02 to 2019-12-31  
- **Total Records:** 5,030 daily entries  

***

## 3. Requirements

**Prerequisites:**
- Python 3.7 or higher  
- pandas library  

**Installation:**
```bash
pip install pandas
```

***

## 4. Execution Steps

1. **Clone** the dataset repository:
   ```bash
   git clone https://github.com/sandeep-tt/tt-intern-dataset.git
   ```

2. **Run** the processing script:
   ```bash
   python process_stock_data.py
   ```

3. **Check outputs** in the `results/` directory. Each ticker will have an individual output file:
   ```
   result_AAPL.csv
   result_AMD.csv
   ...
   result_TSLA.csv
   ```

***

## 5. Output Format

Each output file contains **24 rows** (one per month) and the following columns:

| Column | Description |
|--------|-------------|
| `date` | End-of-month date (YYYY-MM-DD) |
| `open` | Opening price on the first trading day of the month |
| `high` | Highest price during the month |
| `low` | Lowest price during the month |
| `close` | Closing price on the last trading day of the month |
| `adjclose` | Adjusted closing price for the month |
| `volume` | Sum of trading volume during the month |
| `SMA_10`, `SMA_20` | 10- and 20-period Simple Moving Averages of monthly close prices |
| `EMA_10`, `EMA_20` | 10- and 20-period Exponential Moving Averages of monthly close prices |

***

## 6. Monthly Aggregation Logic

- **Open:** Price on the first trading day of the month  
- **Close:** Price on the last trading day of the month  
- **High:** Maximum price in the month  
- **Low:** Minimum price in the month  
- **Volume:** Sum of all trading volumes during the month  

***

## 7. Technical Indicators

### Simple Moving Average (SMA)

\[
SMA_N = \frac{C_1 + C_2 + ... + C_N}{N}
\]

Where \(C_i\) represents the monthly closing prices for the past N periods.

### Exponential Moving Average (EMA)

**Multiplier:**  
\[
\text{Multiplier} = \frac{2}{N + 1}
\]

**Formula:**  
\[
EMA = (Current Price - Previous EMA) \times Multiplier + Previous EMA
\]

The first EMA value is initialized using the corresponding SMA.

***

## 8. Practical Assumptions

This section outlines the practical assumptions made during the implementation of this data processing pipeline.

### 8.1 Data Quality Assumptions

1. **Input Data Integrity**
   - The input CSV file (`output_file.csv`) is assumed to be complete and accessible
   - All required columns (`date`, `volume`, `open`, `high`, `low`, `close`, `adjclose`, `ticker`) are present
   - Date values are in a parseable format (YYYY-MM-DD or similar ISO format)
   - No null or missing values in critical columns (OHLC prices)
   - All price values are positive numbers (no negative or zero prices)

2. **Data Completeness**
   - Each ticker has sufficient data points to generate 24 monthly records (2 years)
   - Missing trading days within a month are acceptable (markets are closed on weekends/holidays)
   - If a month has no trading days, that month is excluded from the output (no forward/backward filling)

3. **Ticker Consistency**
   - All 10 expected tickers (AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA) are present in the dataset
   - Ticker symbols are case-sensitive and match exactly as specified
   - No duplicate ticker-date combinations exist

### 8.2 Business Logic Assumptions

4. **Trading Day Logic**
   - "First trading day" refers to the earliest date with trading data in each calendar month
   - "Last trading day" refers to the latest date with trading data in each calendar month
   - Market holidays and weekends are naturally excluded (no trading data exists for these days)
   - Open and Close prices are snapshots at specific points in time, not averages

5. **Monthly Aggregation**
   - Monthly resampling uses end-of-month (`'ME'`) frequency
   - Each month is treated independently (no cross-month calculations for OHLC)
   - Volume is summed across all trading days in the month
   - High/Low are true maximums/minimums across all trading days in the month

6. **Time Period Assumptions**
   - The dataset covers exactly 24 months (January 2018 to December 2019)
   - Each ticker should produce exactly 24 monthly records
   - Date range is continuous (no large gaps in the dataset)

### 8.3 Technical Indicator Assumptions

7. **SMA Calculation**
   - SMA is calculated using monthly closing prices only
   - For periods with fewer than N months of data, partial calculations are allowed (`min_periods=1`)
   - First SMA value equals the first closing price (SMA of 1 period = that price)
   - SMA window sizes are 10 and 20 periods (months)

8. **EMA Calculation**
   - EMA uses the same monthly closing prices as SMA
   - Multiplier formula: `2 / (Number of Periods + 1)`
   - For the first EMA value, SMA is used as the initial "Previous Day's EMA"
   - Since SMA(1) = first price, the first EMA effectively equals the first closing price
   - EMA window sizes are 10 and 20 periods (months)
   - All EMA calculations use the recursive formula: `EMA = (Price - Prev_EMA) × Multiplier + Prev_EMA`

9. **Indicator Window Handling**
   - For months 1-9: SMA_10 and EMA_10 use available data (partial windows)
   - For months 1-19: SMA_20 and EMA_20 use available data (partial windows)
   - Full window calculations begin at month 10 (SMA_10, EMA_10) and month 20 (SMA_20, EMA_20)

### 8.4 Technical Implementation Assumptions

10. **File System**
    - The script assumes read access to `tt-intern-dataset/output_file.csv`
    - Write access is available for creating the `results/` directory
    - File paths use forward slashes (works on Windows, Linux, macOS)
    - CSV files use UTF-8 encoding (default Pandas behavior)

11. **Data Types**
    - Date column is parsed as datetime objects
    - Price columns (open, high, low, close, adjclose) are float64
    - Volume is integer or float64 (depending on data)
    - Ticker is string/object type

12. **Precision and Rounding**
    - All numeric values preserve original precision from input data
    - No explicit rounding is applied (maintains data accuracy)
    - Output CSV files may show many decimal places based on input precision

### 8.5 Output Format Assumptions

13. **File Naming**
    - Output files follow the convention: `result_{TICKER}.csv` (e.g., `result_AAPL.csv`)
    - Ticker symbols are uppercase in filenames
    - Files are saved in the `results/` directory (created if it doesn't exist)

14. **Output Structure**
    - Each output file contains exactly 24 data rows (one per month) plus header row
    - Rows are sorted chronologically by date (ascending order)
    - Column order: `date`, `open`, `high`, `low`, `close`, `adjclose`, `volume`, `SMA_10`, `SMA_20`, `EMA_10`, `EMA_20`
    - Date format in output: `YYYY-MM-DD` (ISO 8601)

15. **Missing Data Handling**
    - If a month has no trading data, that month is excluded (no row created)
    - If technical indicators cannot be calculated (edge cases), NaN values may appear
    - No interpolation or forward-filling of missing values

### 8.6 Environment Assumptions

16. **Python Environment**
    - Python 3.7 or higher is available
    - Pandas library is installed and accessible
    - Standard library modules (`os`, `typing`) are available
    - No third-party technical analysis libraries are required or used

17. **Performance**
    - Dataset size is manageable in memory (5,030 rows)
    - Processing time is acceptable for interactive use (seconds, not minutes)
    - No distributed processing or database connections required

### 8.7 Edge Cases and Limitations

18. **Known Limitations**
    - Script does not handle stock splits or corporate actions automatically (relies on `adjclose` column)
    - No validation of price relationships (e.g., High >= Low, High >= Open, High >= Close)
    - No handling of data quality issues (negative volumes, impossible price movements)
    - Assumes consistent data structure across all tickers

19. **Error Handling**
    - Script will fail gracefully if input file is missing or malformed
    - No retry logic for file I/O operations
    - No validation of output file creation success beyond basic error handling

***

## 9. Code Structure

| Function | Description |
|-----------|-------------|
| `load_data()` | Loads and parses the input dataset |
| `resample_to_monthly()` | Resamples daily data into monthly OHLC format |
| `calculate_sma()` | Computes Simple Moving Average |
| `calculate_ema()` | Computes Exponential Moving Average |
| `calculate_technical_indicators()` | Applies SMA and EMA across tickers |
| `partition_and_save()` | Saves processed data for each ticker |
| `main()` | Oversees the complete workflow |

***

## 10. Verification Checklist

- 10 output CSV files generated (one per ticker).  
- Each file contains 24 rows plus a header row.  
- All required columns are present and ordered chronologically.  
- SMA/EMA calculations verified: first value equals the closing price.

***

## 11. References

- [Exponential Moving Average (Investopedia)](https://www.investopedia.com/terms/e/ema.asp)  
- [EMA Explanation – Groww](https://groww.in/p/exponential-moving-average)  
- [Pandas Resampling Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html)  
- [Pandas Rolling Windows](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)  
- [Pandas Exponential Weighted Functions](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)


***

## 12. Author

**Atharva Shinde 
Sbjitatharvas@gmail.com**  
