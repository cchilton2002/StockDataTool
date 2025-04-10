import mysql.connector
from settings import DB_CONFIG
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
    
    def create_tables(self, data: pd.DataFrame, ticker: str, start_date: str, end_date: str) -> None:
        if data.empty:
            print("⚠️ No data available for insertion.\n")
            return

        table_name = f"stock_{ticker.lower()}"
        metadata_table = "table_metadata"
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {metadata_table} (
                ticker VARCHAR(10) PRIMARY KEY,
                start_date DATETIME,
                end_date DATETIME
            )
        """)

        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        table_exists = self.cursor.fetchone()

        if not table_exists:
            print(f"Creating new table: {table_name}.\n")
            create_table_query = f"""
                CREATE TABLE {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATETIME,
                    open DECIMAL(10, 2),
                    high DECIMAL(10, 2),
                    low DECIMAL(10, 2),
                    close DECIMAL(10, 2),
                    volume BIGINT
                )
            """
            self.cursor.execute(create_table_query)
        else:
            self.cursor.execute(f"SELECT start_date, end_date FROM {metadata_table} WHERE ticker = %s", (ticker,))
            result = self.cursor.fetchone()

            if result:
                meta_start, meta_end = result
                if meta_start == start_date and meta_end == end_date:
                    print(f"✅ Table {table_name} already contains the correct date range. Skipping update.\n")
                    return

            print(f"🔁 Dates changed — clearing and reinserting data into {table_name}.\n")
            self.cursor.execute(f"DELETE FROM {table_name}")

        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        records = data.to_dict(orient="records")

        insert_query = f"""
            INSERT INTO {table_name} (date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(insert_query, [
            (row["date"], row["open"], row["high"], row["low"], row["close"], row["volume"])
            for row in records
        ])

        self.cursor.execute(f"""
            INSERT INTO {metadata_table} (ticker, start_date, end_date)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE start_date = VALUES(start_date), end_date = VALUES(end_date)
        """, (ticker, start_date, end_date))

        self.conn.commit()
        print(f"✅ Data for {ticker} inserted into {table_name}. Metadata updated.")