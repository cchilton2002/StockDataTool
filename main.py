from real_time import get_real_time_data
from historic_time import get_historical_data, plot_historic_data
import matplotlib as plt
import pandas as pd

if __name__ == "__main__":

    ticker = "GOOGL"
    start_date = "2024-02-01"
    end_date = "2024-06-01"
    
    print("Fetching data...")
    data, ticker = get_historical_data(ticker, start_date, end_date, interval="1day")
    
    if data is not None:
        plot_historic_data(data, ticker)
        # print(data['date'].head())
