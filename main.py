from src.data_loader import fetch_stock_data, save_raw_data
from src.preprocessing import preprocess_data
from src.indicators import add_indicators
from src.model import train_arima
from src.visualization import plot_full_analysis

import os

TICKERS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS"
]

def run_pipeline():
    data = fetch_stock_data(TICKERS)
    save_raw_data(data)

    os.makedirs("data/processed/", exist_ok=True)

    for ticker, df in data.items():
        df = preprocess_data(df)
        df = add_indicators(df)

        plot_full_analysis(df, ticker)

        df.to_csv(f"data/processed/{ticker}.csv")

        forecast = train_arima(df, ticker)
        forecast.to_csv(f"outputs/tables/{ticker}_forecast.csv")

if __name__ == "__main__":
    run_pipeline()