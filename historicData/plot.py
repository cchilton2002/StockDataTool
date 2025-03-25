import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.ticker import NullFormatter
from .indicators import calculate_indicators

def plot_stock_data(
    data:pd.DataFrame, ticker:str, start_date: str, end_date:str, ma:bool, bb:bool, vwap:bool, rsi:bool
) -> None:
    data['date'] = pd.to_datetime(data['date']).dt.date
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()
    
    
    # Calculate the corresponding indicators depending on toggles
    data = calculate_indicators(data, ma, bb, vwap, rsi)
    
    # Filtering data so we only plot between start and end date specified
    filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)].copy()
    
    sns.set_style("whitegrid")
    sns.set_palette("viridis")
    
    ### Font Sizes ###
    axes_labels = 35
    axes_ticks = 22
    title_size = 40
    legend_labels = 20

    # Create figure with price and volume subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    fig.suptitle(f"Stock Price for {ticker.upper()}", fontsize=title_size)
    
    # Plot main stock price (candlestick + line chart)
    plot_candlestick(ax1, filtered_data)
    plot_volume(ax2, filtered_data)
    plot_line(ax1, filtered_data)
    
    if any([ma, bb, vwap]):
        plot_indicator(ax1, filtered_data, ma, bb, vwap)
        ax1.legend(fontsize=legend_labels)


    # Plot RSI in a separate subplot if requested
    if rsi and "RSI" in filtered_data:
        ax3 = ax2.twinx()
        plot_rsi(ax3, filtered_data)
        ax3.set_ylabel("RSI", fontsize=axes_labels, color="orange")
        ax3.tick_params(axis="y", labelsize=axes_ticks)
        ax3.legend(loc="upper right", fontsize=legend_labels)
        
        
    # Formatting axes
    ax1.set_ylabel("Stock Price ($)", fontsize=axes_labels)
    ax2.set_ylabel("Volume", fontsize=axes_labels)

    for ax in [ax1, ax2]:
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.tick_params(axis="y", labelsize=axes_ticks)
        ax.tick_params(axis="x", labelsize=axes_ticks)

    # Format x-axis for dates
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_minor_formatter(NullFormatter())  # Hide minor labels
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()




    
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

def plot_indicator(ax, data, ma, bb, vwap):
    """Plots the selected indicator on the given axis."""
    if ma == True:
        ax.plot(data['date'], data["SMA_200"], color="red", linestyle='-', linewidth=2, label="SMA 200", alpha=0.8) 
        ax.plot(data['date'], data["EMA_200"], linestyle='--', linewidth=2, label="EMA 200", alpha=0.8)
    if bb == True:
        ax.plot(data['date'], data["SMA_20"], linestyle='--', color="purple", linewidth=1.7, label="SMA 20")
        ax.plot(data['date'], data["Upper_BB"], linestyle='-', color="orangered", linewidth=1.1, label="Upper BB")
        ax.plot(data['date'], data["Lower_BB"], linestyle='-', color="limegreen", linewidth=1.1, label="Lower BB")
        ax.fill_between(data['date'], data["Upper_BB"], data["Lower_BB"], color='purple', alpha=0.1, label="BB Range")
    if vwap == True:
        ax.plot(data['date'], data['VWAP'], color="gold", linewidth=2, linestyle="--", label="VWAP")

    

def plot_rsi(ax, data):
    """Plots the RSI indicator on a secondary y-axis (overlapping volume)."""
    
    ax.plot(data['date'], data['RSI'], color="orange", linewidth=2, label="RSI")
    ax.axhline(70, linestyle="--", color="red", alpha=0.7)
    ax.axhline(30, linestyle="--", color="green", alpha=0.7)
    
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=14, colors="orange")
    
    