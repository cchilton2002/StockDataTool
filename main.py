from real_time import get_real_time_data
from historic_time import get_historical_data, plot_historic_data
import matplotlib as plt
import pandas as pd

if __name__ == "__main__":

    ticker = "GOOGL"
    start_date = "2024-02-01"
    end_date = "2024-06-01"
    
    print("Fetching data...")
    data = get_historical_data(ticker, start_date, end_date, interval="1day")
    
    if data is not None:
        # plot_type takes "Bollinger", "Averages" and False values, and plots the corresponding indicators
        # rsi takes Boolean values and toggles the RSI plot on and off
        plot_historic_data(data, ticker, start_date, end_date, plot_type='Bollinger', rsi=True)
