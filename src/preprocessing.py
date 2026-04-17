import pandas as pd

def preprocess_data(df):
    df = df.copy()

    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)

    return df