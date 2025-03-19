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

        
def plot_historic_data(data, ticker, start_date, end_date, plot_type='Averages', rsi:bool=True):
    data['date'] = pd.to_datetime(data['date']).dt.date
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()
    
    data = calculate_indicators(data, plot_type, rsi)
    
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)].copy()
    
    
    # Use a seaborn style for a nicer look
    sns.set_style("whitegrid")
    sns.set_palette("viridis")  # Choose a color palette 

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f"Stock Price and Volume for {ticker}", fontsize=24)
    
    plot_candlestick(ax1, filtered_data)
    plot_volume(ax2, filtered_data)
    plot_line(ax1, filtered_data)
    if plot_type in ['Averages', 'Bollinger']:
        plot_indicator(ax1, filtered_data, plot_type)
    else: 
        pass

    if rsi==True:
        ax3 = ax2.twinx()
        plot_rsi(ax3, filtered_data)
        ax3.set_ylabel("RSI", fontsize=16, color="orange")
    

    ax1.set_ylabel("Stock Price ($)", fontsize=16)
    ax2.set_ylabel("Volume", fontsize=16)

    for ax in [ax1, ax2]:
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', labelsize=14)
    
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_minor_locator(NullLocator())
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
    plt.show()


def calculate_indicators(data, plot_type, rsi):
    """Ensures all necessary columns exist before filtering data."""
    if rsi==True:
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
    if plot_type=='Bollinger':      
        # Always compute Bollinger Bands (even if not used)
        data["SMA_20"] = data["close"].rolling(window=20).mean()
        data["Upper_BB"] = data["SMA_20"] + (data["close"].rolling(window=20).std() * 2)
        data["Lower_BB"] = data["SMA_20"] - (data["close"].rolling(window=20).std() * 2)
    elif plot_type=='Averages':
        # Compute SMA and EMA for all cases
        data["SMA_200"] = data["close"].rolling(window=200).mean()
        data["EMA_200"] = data['close'].ewm(span=200, adjust=False).mean()
    return data

def plot_candlestick(ax, data):
    """Plots a candlestick chart on the given axis."""
    bar_width = 1
    wick_width = 1.5
    
    for date, open_, close, low, high in zip(data['date'], data['open'], data['close'], data['low'], data['high']):
        color = 'green' if close > open_ else 'red'
        ax.vlines(x=date, ymin=low, ymax=high, color=color, linewidth=wick_width)
        ax.bar(x=date, bottom=min(open_, close), height=abs(close - open_), color=color, width=bar_width)


def plot_line(ax, data):
    ax.plot(data['date'], data['close'], color='grey', alpha=0.8, linewidth=1.6)
    
def plot_volume(ax, data):
    """Plots the volume bar chart on the given axis."""
    ax.bar(data['date'], data['volume'], color=sns.color_palette()[0], width=0.8)

def plot_indicator(ax, data, plot_type):
    """Plots the selected indicator on the given axis."""
    if plot_type == "Averages":
        ax.plot(data['date'], data["SMA_200"], color="red", linestyle='-', linewidth=2, label="SMA 200", alpha=0.8) 
        ax.plot(data['date'], data["EMA_200"], linestyle='--', linewidth=2, label="EMA 200", alpha=0.8)
    elif plot_type == "Bollinger":
        ax.plot(data['date'], data["SMA_20"], linestyle='--', color="purple", linewidth=1.7, label="SMA 20")
        ax.plot(data['date'], data["Upper_BB"], linestyle='-', color="orangered", linewidth=1.1, label="Upper BB")
        ax.plot(data['date'], data["Lower_BB"], linestyle='-', color="limegreen", linewidth=1.1, label="Lower BB")
        ax.fill_between(data['date'], data["Upper_BB"], data["Lower_BB"], color='purple', alpha=0.1, label="BB Range")
    ax.legend(fontsize=16)
    

def plot_rsi(ax, data):
    """Plots the RSI indicator on a secondary y-axis (overlapping volume)."""
    
    ax.plot(data['date'], data['RSI'], color="orange", linewidth=2, label="RSI")
    ax.axhline(70, linestyle="--", color="red", alpha=0.7)
    ax.axhline(30, linestyle="--", color="green", alpha=0.7)
    
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=14, colors="orange")
    ax.legend(loc="upper right", fontsize=12)

