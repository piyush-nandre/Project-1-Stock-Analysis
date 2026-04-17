import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import os

app = dash.Dash(__name__)

TICKERS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"]

app.layout = html.Div([
    html.H1("Stock Market Dashboard"),

    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': t, 'value': t} for t in TICKERS],
        value=TICKERS[0]
    ),

    dcc.Graph(id='stock-chart')
])


@app.callback(
    Output('stock-chart', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_chart(ticker):
    import pandas as pd
    import plotly.graph_objects as go
    import os

    data_path = f"data/processed/{ticker}.csv"
    forecast_path = f"outputs/tables/{ticker}_forecast.csv"

    # Always initialize fig FIRST
    fig = go.Figure()

    if not os.path.exists(data_path):
        return fig

    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    start_date = df['Date'].max() - pd.DateOffset(months=6)
    end_date = df['Date'].max()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Price"
    ))

    # Moving averages
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name='SMA 20'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], name='SMA 50'))

    # Forecast
    if os.path.exists(forecast_path):
        forecast = pd.read_csv(forecast_path)
        forecast.index = pd.date_range(start=df['Date'].max(), periods=len(forecast), freq='B')

        fig.add_trace(go.Scatter(
            x=forecast.index,
            y=forecast.iloc[:, 0],
            mode='lines',
            name='Forecast',
            line=dict(dash='dash')
        ))

    # Layout (AFTER fig is created)
    fig.update_layout(
    title=f"{ticker} Price + Forecast",
    template="plotly_white",
    height=700,
    xaxis=dict(
        range=[start_date, end_date],  # 👈 KEY FIX
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all", label="All")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

    return fig

if __name__ == "__main__":
    app.run(debug=True)