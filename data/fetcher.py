import requests
import pandas as pd
from datetime import timedelta
from typing import Optional
from config import BASE_URL, API_KEY

from .database import DatabaseManager

class StockDataManager:
    def __init__(self, ticker: str, start_date: str, end_date: str, interval: str):
        self.ticker = ticker
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.interval = interval
        self.data = None

    def get_historical_data(self, save_data: bool = True) -> Optional[pd.DataFrame]:
        db = DatabaseManager()

        print("Checking metadata table...")
        meta = db.get_metadata(self.ticker)

        user_start = self.start_date.strftime("%Y-%m-%d")
        user_end = self.end_date.strftime("%Y-%m-%d")

        if meta:
            db_start = meta["start_date"].strftime("%Y-%m-%d")
            db_end = meta["end_date"].strftime("%Y-%m-%d")

            if db_start == user_start and db_end == user_end:
                print("Metadata matches. Loading data from database...")
                self.data = db.fetch_stock_data(self.ticker)
                return self.data
            else:
                print("Metadata mismatch. Performing API call and updating DB.")
        else:
            print("No metadata found. Performing API call.")

        # Fallback to API
        return self._fetch_from_api_and_save(db, save_data)
    
    
    def _fetch_from_api_and_save(self, db, save_data):
        print("Fetching data from API...")
        try:
            endpoint = f"{BASE_URL}/daily/{self.ticker}/prices"
            params = {
                "startDate": self.start_date - timedelta(days=(200 / 0.68)),
                "endDate": self.end_date,
                "format": "json",
                "token": API_KEY,
            }
            if self.interval != "1day":
                params["resampleFreq"] = self.interval

            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = pd.DataFrame(response.json())

            self.data = data

            if save_data:
                db.create_tables(data, self.ticker, self.start_date.strftime("%Y-%m-%d"), self.end_date.strftime("%Y-%m-%d"))
                print("Data saved to DB.")

            return self.data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the data: {e}")
            return None


    
            