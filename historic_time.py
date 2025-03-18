import requests 
import pandas as pd
from config import API_KEY
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import NullLocator
from matplotlib.gridspec import GridSpec
import seaborn as sns
from datetime import timedelta

# Tiingo is the website we will use for the API calls 
BASE_URL = "https://api.tiingo.com/tiingo"


def get_historical_data(ticker, start_date, end_date, interval="1hour"):
    endpoint = f"{BASE_URL}/daily/{ticker}/prices"

    start_date = pd.to_datetime(start_date)
    
    params = {
        "startDate": start_date - timedelta(days=(200/0.68)),
        "endDate": end_date,
        "format": "json",
        "token": API_KEY  
    }
    # Add resampleFreq for intraday data, this takes specific values (SEE TIINGO DOCUMENTATION)
    if interval != "1day":
        params["resampleFreq"] = interval

    try:
        response = requests.get(endpoint, params=params) # Get the data from the API call
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching the data: {e}")
        return None



def plot_historic_data(data, ticker, start_date, end_date):
    data['date'] = pd.to_datetime(data['date']).dt.date
    
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()
    
    # Compute moving averages manually
    data["SMA_200"] = data["close"].rolling(window=200).mean()

    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)].copy()
    
    # Use a seaborn style for a nicer look
    sns.set_style("whitegrid")
    sns.set_palette("viridis")  # Choose a color palette 

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    ax1.cla() # clear axis 1
    ax2.cla() # clear axis 2
    fig.suptitle(f"Stock Price and Volume for {ticker}", fontsize=24) # Add a title

    bar_width = 0.7  # Adjusted for better spacing
    # Price chart (ax1)
    for date, open_, close, low, high in zip(filtered_data['date'], filtered_data['open'], filtered_data['close'], filtered_data['low'], filtered_data['high']):
        color = 'green' if close > open_ else 'red'  # More traditional colors
        bottom = min(open_, close)
        height = abs(close - open_)
        # Plot the wick 
        ax1.vlines(x=date, ymin=low, ymax=high, color=color, linewidth=1.5)
        # Plot the candle body
        ax1.bar(x=date, bottom=bottom, height=height, color=color, width=1)

       
    filtered_data["EMA_200"] = filtered_data['close'].ewm(span=200, adjust=False).mean() #calculate ema based on close price.

    ax1.plot(filtered_data['date'], filtered_data['close'], color='grey', alpha=0.8, linewidth=1.6)
    ax1.plot(filtered_data['date'], filtered_data['EMA_200'], linestyle='--', linewidth=2, label="EMA 200", alpha=0.8)
    ax1.plot(filtered_data['date'], filtered_data["SMA_200"], color="red", linestyle='-', linewidth=2, label="SMA 200", alpha=0.8) 

    ax2.bar(filtered_data['date'], filtered_data['volume'], color=sns.color_palette()[0], width=0.8) # Use a color from the palette

    # Better formatting of the ticks 
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_minor_locator(NullLocator())
    ax1.legend(fontsize=16)


    ax1.set_ylabel("Stock Prce ($)", fontsize=16)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.tick_params(axis='y', labelsize=14) # Adjust tick label size

    # Volume chart (ax2)
    ax2.set_ylabel("Volume", fontsize=16)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.tick_params(axis='y', labelsize=14)
    ax2.tick_params(axis='x', labelsize=14)

    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax2.xaxis.set_minor_locator(NullLocator())


    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust tight_layout to fit title
    plt.show()
