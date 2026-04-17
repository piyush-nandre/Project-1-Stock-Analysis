from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import os

def train_arima(df, ticker):
    df = df.dropna()

    model = ARIMA(df['Close'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=30)

    os.makedirs("outputs/models/", exist_ok=True)
    model_fit.save(f"outputs/models/{ticker}_arima.pkl")

    return forecast