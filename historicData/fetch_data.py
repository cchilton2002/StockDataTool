import pandas as pd
import requests
from historicData.database import create_tables
from historicData.indicators import fetch_stock_data
from config import API_KEY, BASE_URL
from datetime import timedelta
from typing import Optional, List, Dict, Any



def get_historical_data(
    ticker: str, start_date: str, end_date: str, interval: str, save_data:bool 
) -> Optional[List[Dict[str, Any]]]:
    
    endpoint = f"{BASE_URL}/daily/{ticker}/prices"

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    params = {
        "startDate": start_date - timedelta(days=(200/0.68)),
        "endDate": end_date,
        "format": "json",
        "token": API_KEY  
    }
    # Add resampleFreq for intraday data, this takes specific values (SEE TIINGO DOCUMENTATION)
    if interval != "1day":
        params["resampleFreq"] = interval

    try:
        response = requests.get(endpoint, params=params) # Get the data from the API call
        response.raise_for_status()
        data = pd.DataFrame(response.json())
        
        if save_data:
            create_tables(
                data, 
                ticker, 
                start_date.strftime("%Y-%m-%d"),  # Convert Timestamp to string
                end_date.strftime("%Y-%m-%d")     # Convert Timestamp to string
            )
            data_db = fetch_stock_data(ticker)
            print("Used DB data. \n")
            return data_db
        else:
            return data
    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching the data: {e}")
        return None