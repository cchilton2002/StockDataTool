import requests 
import pandas as pd
from config import API_KEY

BASE_URL = "https://api.tiingo.com/tiingo"


def get_historical_data(ticker, start_date, end_date, interval="1hour"):

    endpoint = f"{BASE_URL}/daily/{ticker}/prices"


    params = {
        "startDate": start_date,
        "endDate": end_date,
        "format": "json",
        "token": API_KEY  # Pass the API key as a query parameter
    }

    # Add resampleFreq for intraday data
    if interval != "1day":
        params["resampleFreq"] = interval

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching the data: {e}")
        return None