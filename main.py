from real_time import get_real_time_data
from historicData.fetch_data import get_historical_data
import pandas as pd
from historicData.plot import plot_stock_data


if __name__ == "__main__":
    # Ticker: is the stock which you would like to view historical data for
    # Start and end date takes the format<%Y-%m-%d>
    ticker = "GOOGL"
    start_date = "2008-01-01"
    end_date = "2009-03-01"
    
    print("Fetching data...")
    # Fetch the data from the API
    # If save_data is True then the data will be stored in a MySQL database
    # Unless the dates are changed the subsequent analysis will pull data from this DB
    data = get_historical_data(ticker, start_date, end_date, interval="1day", save_data=False)
    
    if data is not None:
        # ma: Moving averages (SMA 200 and EMA 200)
        # bb: Bollinger Bands
        # vwap: Volume weighted average price
        # rsi: Relative strength index
        # All of these indicators can be toggled with a boolean switch
        plot_stock_data(data, ticker=ticker, start_date=start_date, end_date=end_date,ma=False, bb=True, vwap=False, rsi=True)
    

