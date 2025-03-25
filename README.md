# Stock Data Visualization Tool

This Python program retrieves historical stock data using Tiingo for API calls and visualises it with `matplotlib`. It displays candlestick-like charts of stock prices along with volume data, providing a clear overview of stock performance over time.

## Features

* **Historical Data Retrieval:** Fetches stock data from Tiingo.
* **Candlestick-like Charts:** Visualises stock price movements with open, close, high, and low values.
* **Volume Charts:** Displays trading volume alongside price data.
* **Customisable Plotting:** Uses `matplotlib` and `seaborn` for enhanced visualisation and styling.
* **Toggle Indicators** Toggle useful indicators such as moving averages (EMA 200, SMA 200), Bollinger bands, RSI and VWAP.


## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd StockDataTool
    ```
2.  **Create a API key Tiingo:**
    Create an account on Tingo and add your API key to the `config.py` script

3.  **Ensure MySQL information:**
    For this program I used MySQL as the database management system, required user specific info can be found in `config.py`

4.  **Create `.env` file:**
    Create a `.env` file that has all the required user specifc information that is needed in `config.py`, eg. API_KEY.

4.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

5.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Modify `main.py`:**
    * Change the `ticker`, `start_date`, and `end_date` variables to retrieve and visualise different stock data.
    * Change the `interval` variable to change the data interval.

    ```python
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-03-01"
    interval = "1day" 
    ```

    * Depending on whether you want to save the data in a database, toggle the ```save_data=True```.
    * If you would like different indicators displayed toggle the specific indicators, ma: moving averages, bb: bollinger bands,
      vwap: volume weighted average price and rsi: relative strength index.

2.  **Run the `main.py` script:**

    ```bash
    python main.py
    ```

3.  **View the plot:**
    * A `matplotlib` window will display the stock price and volume chart.

## Files

* `main.py`: The main script that retrieves data and generates the plot.
* `plot.py`: Contains the functions and specific formatting for the plot itself.
* `indicators.py`: Fetches data from the database if used and defines the function to calculate the specific indicator values.
* `database.py`: Defines the function for creating the tables within our database for each dataset.
* `fetch_data.py`: This file calls the Tiingo API fetch the data as well as define whether to use database data or not 
                   depending on user choices.
* `requirements.txt`: Lists the required Python packages.
* `config.py`: Contains the API KEY and other sensitive info for the program.
* `.gitignore`: Specifies files and directories to ignore in Git.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.
