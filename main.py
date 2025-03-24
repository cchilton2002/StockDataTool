from real_time import get_real_time_data
from historicData.fetch_data import get_historical_data
import matplotlib as plt
import pandas as pd
from historicData.plot import plot_stock_data
from historicData.indicators import calculate_indicators, fetch_stock_data
from historicData.database import create_tables


if __name__ == "__main__":

    ticker = "GOOGL"
    start_date = "2008-01-01"
    end_date = "2009-03-01"
    
    print("Fetching data...")
    
    
    
    data = get_historical_data(ticker, start_date, end_date, interval="1day", save_data=False)
    
    plot_stock_data(data, ticker=ticker, start_date=start_date, end_date=end_date,ma=False, bb=True, vwap=False, rsi=True)
    
    
    
    
    # if data is not None:
        # ma: Moving averages (SMA 200 and EMA 200)
        # bb: Bollinger Bands
        # vwap: Volume weighted average price
        # rsi: Relative strength index
        # All of these indicators can be toggled with a boolean switch
        # plot_stock_data(data, ticker, start_date, end_date, ma=True, bb=True, vwap=True, rsi=True)
