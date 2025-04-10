import pandas as pd
from settings import BASE_URL, API_KEY

class StockDataManager:
    def __init__(self, ticker: str, start_date: str, end_date: str, interval: str):
        self.ticker = ticker
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.interval = interval
        self.data = None

    def get_historical_data(self, save_data: bool = True) -> Optional[pd.DataFrame]:
        if save_data:
            print("🔍 Checking database for stored data...")
            self.data = fetch_stock_data(self.ticker)

            if self.data is not None and not self.data.empty:
                print("✅ Loaded data from database.\n")
                return self.data
            else:
                print("⚠️ No data found in DB. Switching to API call...")

        # ✅ Only run this if we're not saving OR no data was found above
        print("🌐 Fetching data from API...")
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
                create_tables(
                    data,
                    self.ticker,
                    self.start_date.strftime("%Y-%m-%d"),
                    self.end_date.strftime("%Y-%m-%d"),
                )
                print("💾 Data saved to DB.")

            return self.data

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching the data: {e}")
            return None
 
        