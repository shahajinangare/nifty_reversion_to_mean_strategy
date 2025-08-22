# Nifty 50 Stock Data Extraction Guide

## Overview
This guide provides Python code to extract the last 5 years of daily closing prices for all 50 Nifty stocks using free data sources.

## Prerequisites
```bash
pip install yfinance pandas numpy
```

## Current Nifty 50 Stocks (as of March 28, 2025)
The script includes all 50 current constituents:
- Financial Services: HDFCBANK, ICICIBANK, AXISBANK, KOTAKBANK, SBIN, BAJFINANCE, BAJAJFINSV, HDFCLIFE, SBILIFE, INDUSINDBK, SHRIRAMFIN, JIOFIN
- Information Technology: TCS, INFY, HCLTECH, TECHM, WIPRO
- Oil & Gas: RELIANCE, ONGC
- Consumer Goods: HINDUNILVR, ITC, NESTLEIND, TATACONSUM
- Automobile: TATAMOTORS, M&M, MARUTI, BAJAJ-AUTO, HEROMOTOCO, EICHERMOT
- Healthcare: SUNPHARMA, DRREDDY, CIPLA, APOLLOHOSP
- And 20 more stocks across various sectors

## Quick Start (Simple Version)
```python
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Nifty 50 symbols with .NS suffix for Yahoo Finance
symbols = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "ETERNAL.NS",
    "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS",
    "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",
    "ITC.NS", "JIOFIN.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "SBIN.NS",
    "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

# Date range: last 5 years
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

# Download data for all symbols
data = yf.download(symbols, start=start_date, end=end_date, group_by='ticker')

# Extract only closing prices
closing_prices = data.xs('Close', axis=1, level=1)

# Clean column names (remove .NS)
closing_prices.columns = [col.replace('.NS', '') for col in closing_prices.columns]

# Save to CSV
closing_prices.to_csv('nifty50_closing_prices.csv')

print(f"Data shape: {closing_prices.shape}")
print(f"Date range: {closing_prices.index.min()} to {closing_prices.index.max()}")
print("Data saved as 'nifty50_closing_prices.csv'")
```

## Advanced Features
The comprehensive script (`nifty50_data_extractor.py`) includes:

### Error Handling & Rate Limiting
- Handles failed downloads gracefully
- Implements delays between API calls
- Provides detailed progress reporting
- Manages missing data appropriately

### Data Quality Features
- Validates downloaded data
- Reports missing values
- Provides comprehensive statistics
- Auto-adjusts prices for splits/dividends

### Additional Metrics (Optional)
```python
def calculate_technical_indicators(df):
    """Add technical indicators to the dataset"""
    for col in df.columns:
        df[f'{col}_SMA_20'] = df[col].rolling(20).mean()
        df[f'{col}_SMA_50'] = df[col].rolling(50).mean()
        df[f'{col}_Returns'] = df[col].pct_change()
        df[f'{col}_Volatility'] = df[f'{col}_Returns'].rolling(20).std()
    return df
```

## Usage Instructions

### Method 1: Run the Complete Script
```bash
python nifty50_data_extractor.py
```
This will:
- Download 5 years of daily data
- Handle errors automatically
- Create a comprehensive CSV file
- Provide detailed statistics

### Method 2: Use Simple Version
```bash
python nifty50_simple.py
```
Quick and straightforward download with minimal code.

### Method 3: Individual Stock Download
```python
import yfinance as yf

# Download single stock
reliance = yf.Ticker("RELIANCE.NS")
data = reliance.history(period="5y")
print(data.head())
```

## Data Output Format
The resulting CSV file contains:
- **Rows**: Trading dates (Monday to Friday, excluding holidays)
- **Columns**: 50 Nifty stocks (symbol names without .NS suffix)
- **Values**: Daily closing prices adjusted for splits and dividends
- **Size**: Approximately 1,300+ rows × 50 columns

## Key Features of Yahoo Finance API
✅ **Free to use** - No API key required  
✅ **Comprehensive data** - OHLCV + adjusted prices  
✅ **Indian market support** - NSE stocks with .NS suffix  
✅ **Historical data** - Up to 10+ years available  
✅ **Reliable source** - Used by millions globally  

## Alternative Free Sources
1. **NSE Official Data**: Direct from NSE website
2. **Alpha Vantage**: Free tier with API key
3. **Quandl/Nasdaq Data Link**: Limited free access
4. **NSEPython**: Python library for NSE data

## Data Validation Tips
```python
# Check data quality
print(f"Total missing values: {df.isnull().sum().sum()}")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Number of trading days: {len(df)}")

# Verify price ranges (detect outliers)
for col in df.columns:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    outliers = df[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)][col]
    if len(outliers) > 0:
        print(f"{col}: {len(outliers)} potential outliers")
```

## Limitations & Considerations
- **Rate limits**: Yahoo Finance may limit requests (hence the delays)
- **Data accuracy**: Prices are adjusted but may have occasional gaps
- **Weekend/holidays**: No trading data on non-trading days
- **Corporate actions**: Stock splits and dividends are auto-adjusted
- **Recently added stocks**: Some newer Nifty additions may have limited history

## For Production Use
Consider upgrading to paid data providers for:
- Real-time data feeds
- Higher request limits  
- Guaranteed data quality
- Professional support
- Additional data points (fundamental ratios, news, etc.)

## Troubleshooting
```python
# If downloads fail, try individual downloads
failed_stocks = []
for symbol in symbols:
    try:
        data = yf.download(symbol, period="5y")
        if data.empty:
            failed_stocks.append(symbol)
    except:
        failed_stocks.append(symbol)

print(f"Failed downloads: {failed_stocks}")
```

This guide provides everything needed to extract Nifty 50 stock data for quantitative modeling using free Python libraries.
