import requests 
import pandas as pd
from config import API_KEY
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import NullLocator
from matplotlib.gridspec import GridSpec
import seaborn as sns

BASE_URL = "https://api.tiingo.com/tiingo"


def get_historical_data(ticker, start_date, end_date, interval="1hour"):

    endpoint = f"{BASE_URL}/daily/{ticker}/prices"


    params = {
        "startDate": start_date,
        "endDate": end_date,
        "format": "json",
        "token": API_KEY  # Pass the API key as a query parameter
    }

    # Add resampleFreq for intraday data
    if interval != "1day":
        params["resampleFreq"] = interval

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data), ticker
    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching the data: {e}")
        return None



def plot_historic_data(data, ticker):
    data['date'] = pd.to_datetime(data['date']).dt.date

    # Use a seaborn style for a nicer look
    sns.set_style("whitegrid")
    sns.set_palette("viridis")  # Choose a color palette (e.g., viridis, pastel, deep)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    ax1.cla() # clear axis 1
    ax2.cla() # clear axis 2
    fig.suptitle(f"Stock Price and Volume for {ticker}", fontsize=16) # Add a title

    bar_width = 0.7  # Adjusted for better spacing

    # Price chart (ax1)
    for date, open_, close, low, high in zip(data['date'], data['open'], data['close'], data['low'], data['high']):
        color = 'green' if close > open_ else 'red'  # More traditional colors
        bottom = min(open_, close)
        height = abs(close - open_)

        ax1.vlines(x=date, ymin=low, ymax=high, color=color, linewidth=1)
        ax1.bar(x=date, bottom=bottom, height=height, color=color, width=bar_width)

    ax1.plot(data['date'], data['close'], color='gray', linewidth=1.5, alpha=0.9, label='Closing Price')

    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_minor_locator(NullLocator())

    thresh = 40
    y_min = data['low'].min() - data['low'].min() / thresh
    y_max = data['high'].max() + data['high'].max() / thresh
    ax1.set_ylim(y_min, y_max)

    ax1.set_ylabel("Stock Prce ($)", fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.tick_params(axis='y', labelsize=10) # Adjust tick label size

    # Volume chart (ax2)
    ax2.bar(data['date'], data['volume'], color=sns.color_palette()[0], width=bar_width) # Use a color from the palette
    ax2.set_ylabel("Volume", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.tick_params(axis='y', labelsize=10)

    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax2.xaxis.set_minor_locator(NullLocator())

    # ax2.set_xlabel("Date", fontsize=12)
    # ax2.tick_params(axis='x', labelsize=10, rotation=45) # Rotate x-axis labels

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust tight_layout to fit title
    plt.show()
