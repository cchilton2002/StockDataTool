from real_time import get_real_time_data
from historic_time import get_historical_data, plot_historic_data
import matplotlib as plt
import pandas as pd

if __name__ == "__main__":

    ticker = "AAPL"
    start_date = "2024-02-01"
    end_date = "2024-06-01"
    
    print("Fetching data...")
    data = get_historical_data(ticker, start_date, end_date, interval="1day")
    
    if data is not None:
        # ma: Moving averages (SMA 200 and EMA 200)
        # bb: Bollinger Bands
        # vwap: Volume weighted average price
        # rsi: Relative strength index
        # All of these indicators can be toggled with a boolean switch
        plot_historic_data(data, ticker, start_date, end_date, ma=True, bb=False, vwap=False, rsi=False)
