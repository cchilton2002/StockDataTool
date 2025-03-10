# import the necessary libraries

import requests 
import pandas as pd
from config import API_KEY

BASE_URL = "https://api.tiingo.com/tiingo"

HEADERS = {
    "Content-Type" : "application/json",
    "Authorization" : f"Token {API_KEY}"
}

def get_real_time_data(ticker):
    # Fetch real time stock data for a giver ticker (symbol)

    endpoint = f"{BASE_URL}/daily/{ticker}/prices"
    params = {
        "tickers" : ticker,
        "format" : "json"
    }

    try:
        response = requests.get(endpoint, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except request.exceptions.RequestException as e:
        print(f"Error fetching the real-time data: {e}")
        return None

        
