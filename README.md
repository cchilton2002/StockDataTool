# Stock Data Visualization Tool

This Python program retrieves historical stock data using Tiingo for API calls and visualises it with `matplotlib`. It displays candlestick-like charts of stock prices along with volume data, providing a clear overview of stock performance over time.

## Features

* **Historical Data Retrieval:** Fetches stock data from Tiingo.
* **Candlestick-like Charts:** Visualises stock price movements with open, close, high, and low values.
* **Volume Charts:** Displays trading volume alongside price data.
* **Customizable Plotting:** Uses `matplotlib` and `seaborn` for enhanced visualisation and styling.
* **Date-based X-Axis:** Provides clear date labels for time-series analysis.
* **Clear Title:** Displays the ticker symbol in the title.

## Prerequisites

* Python 3.x
* `pandas`
* `matplotlib`
* `seaborn`

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd StockDataTool
    ```
2.  **Create a API key Tiingo:**
    Create an account on Tingo and add your API key to the `config.py` script

3.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the `main.py` script:**

    ```bash
    python main.py
    ```

2.  **Modify `main.py`:**
    * Change the `ticker`, `start_date`, and `end_date` variables to retrieve and visualise different stock data.
    * Change the `interval` variable to change the data interval.

    ```python
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-03-01"
    interval = "1day" 
    ```

3.  **View the plot:**
    * A `matplotlib` window will display the stock price and volume chart.

## Files

* `main.py`: The main script that retrieves data and generates the plot.
* `historic_time.py`: Contains the functions for retrieving and plotting historical data.
* `real_time.py`: Contains the functions which retrieve real time data of the stock.
* `requirements.txt`: Lists the required Python packages.
* `.gitignore`: Specifies files and directories to ignore in Git.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.
