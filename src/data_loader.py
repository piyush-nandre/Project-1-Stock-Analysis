import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(tickers, start="2020-01-01", end=None):
    data = {}

    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end)
        df.dropna(inplace=True)
        df["Ticker"] = ticker
        data[ticker] = df

    return data


def save_raw_data(data_dict, path="data/raw/"):
    os.makedirs(path, exist_ok=True)

    for ticker, df in data_dict.items():
        df.to_csv(f"{path}{ticker}.csv")