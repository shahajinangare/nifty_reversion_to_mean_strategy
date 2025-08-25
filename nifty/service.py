# Simple version - Quick start
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import io

class ClosingPricesService:
    def get_nifty50_closing_price():
        csv_folder_path = 'csv_files'
        # Nifty 50 symbols
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
        # closing_prices.to_csv('../'+csv_folder_path+'/nifty50_closing_prices.csv')

        print(f"Data shape: {closing_prices.shape}")
        print(f"Date range: {closing_prices.index.min()} to {closing_prices.index.max()}")
        print("Data saved as 'nifty50_closing_prices.csv'")

        return closing_prices