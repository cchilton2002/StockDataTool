from real_time import get_real_time_data
from historic_time import get_historical_data

if __name__ == "__main__":


    real_time_data = get_real_time_data("AAPL")
    if real_time_data is not None:
        print("Real time data: ")
        print(real_time_data)


    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-02-01"
    
    print("Fetching daily data...")
    daily_data = get_historical_data(ticker, start_date, end_date, interval="1day")
    if daily_data is not None:
        print("Daily Data:")
        print(daily_data)

    # Historical data with weekly interval
    print("\nFetching weekly data...")
    hourly_data = get_historical_data(ticker, start_date, end_date, interval="weekly")
    if hourly_data is not None:
        print("Weekly Data:")
        print(hourly_data)