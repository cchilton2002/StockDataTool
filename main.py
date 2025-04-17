# from real_time import get_real_time_data
# from historicData.fetch_data import get_historical_data
# import pandas as pd
# from historicData.plot import plot_stock_data


from data import StockDataManager
from visualisation.plotter import StockPlotter

# --- Parameters (could later be user input or CLI args) ---
TICKER = "AAPL"
START_DATE = "2022-01-01"
END_DATE = "2022-05-31"
INTERVAL = "1day"

# Indicator toggles
PLOT_MA = True
PLOT_BB = True
PLOT_VWAP = False
PLOT_RSI = True

def main():
    print("Starting stock data pipeline...\n")
    
    # Step 1: Fetch the data
    manager = StockDataManager(ticker=TICKER, start_date=START_DATE, end_date=END_DATE, interval=INTERVAL)
    data = manager.get_historical_data(save_data=True)
    

    if data is None or data.empty:
        print("No data available to plot.")
        return
    
    # Step 2: Plot the data with indicators
    plotter = StockPlotter(data, TICKER, START_DATE, END_DATE)
    plotter.plot(ma=PLOT_MA, bb=PLOT_BB, vwap=PLOT_VWAP, rsi=PLOT_RSI)

if __name__ == "__main__":
    main()

    

