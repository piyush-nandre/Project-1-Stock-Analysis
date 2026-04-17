import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def plot_full_analysis(df, ticker):
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2]
    )

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ), row=1, col=1)

    # Moving averages
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name='SMA 20'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], name='SMA 50'), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI'), row=2, col=1)

    # Volatility
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Volatility'], name='Volatility'), row=3, col=1)

    fig.update_layout(title=f"{ticker} Full Analysis", height=900)

    os.makedirs("outputs/figures/", exist_ok=True)
    fig.write_html(f"outputs/figures/{ticker}_analysis.html")

    return fig