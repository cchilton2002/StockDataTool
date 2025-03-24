import mysql.connector
from config import DB_CONFIG
from typing import List, Dict, Any
import pandas as pd
from datetime import timedelta, datetime


def create_tables(
    data: pd.DataFrame, ticker:str, start_date:str, end_date:str
) -> None:
    """
    Stores fetched stock data into a dynamically named MySQL table.
    """
    
    if data.empty:
        print("⚠️ No data available for insertion.")
        return
    

    table_name = f"stock_{ticker.lower()}"
    metadata_table = "table_metadata"
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {metadata_table} (
                ticker VARCHAR(10) PRIMARY KEY,
                start_date DATETIME,
                end_date DATETIME
            )
        """)
        
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            # ✅ If the table doesn't exist, create it
            print(f"🆕 Creating new table: {table_name}")
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
            cursor.execute(create_table_query)
        else: 
            # ✅ Fetch current min and max dates from the table
            cursor.execute(f"SELECT start_date, end_date FROM {metadata_table} WHERE ticker = %s", (ticker,))
            result = cursor.fetchone()
            
            if result:
                meta_start, meta_end = result
            
                if meta_start == start_date and meta_end == end_date:
                    print(f"✅ Table {table_name} already contains the correct date range. Skipping update.")
                    cursor.close()
                    conn.close()
                    return
            
            print(f"The start and end dates have been changed, reinserting {table_name} data. \n")
            cursor.execute(f"DELETE FROM {table_name}")
        
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        records = data.to_dict(orient="records")
        
        
        # ✅ Insert new data
        insert_query = f"""
            INSERT INTO {table_name} (date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, [(row["date"], row["open"], row["high"], row["low"], row["close"], row["volume"]) for row in records])
        
        cursor.execute(f"""
            INSERT INTO {metadata_table} (ticker, start_date, end_date)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE start_date = VALUES(start_date), end_date = VALUES(end_date)
        """, (ticker, start_date, end_date))

        conn.commit()
        print(f"✅ Data for {ticker} inserted into {table_name}. Metadata updated.")

    except mysql.connector.Error as e:
        print(f"❌ MySQL error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()