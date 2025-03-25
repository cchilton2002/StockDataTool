import pandas as pd
import mysql.connector
from config import DB_CONFIG
from typing import Optional

def fetch_stock_data(
    ticker: str
) -> Optional[pd.DataFrame]:
    table_name = f"stock_{ticker.lower()}"
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = f"""
            SELECT * FROM {table_name} ORDER BY date ASC
        """
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]

        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        df = pd.DataFrame(rows, columns=columns)
        return df
    
    except mysql.connector.Error as e:
        print(f"MySql error: {e}")


def calculate_indicators(
    data: pd.DataFrame, ma: bool, bb: bool, vwap: bool, rsi: bool
    ):
    if rsi:
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
    if bb:      
        # Always compute Bollinger Bands (even if not used)
        data["SMA_20"] = data["close"].rolling(window=20).mean()
        data["Upper_BB"] = data["SMA_20"] + (data["close"].rolling(window=20).std() * 2)
        data["Lower_BB"] = data["SMA_20"] - (data["close"].rolling(window=20).std() * 2)
    if ma:
        # Compute SMA and EMA for all cases
        data["SMA_200"] = data["close"].rolling(window=200).mean()
        data["EMA_200"] = data['close'].ewm(span=200, adjust=False).mean()
    if vwap:
        vwap_numerator = (data['close'] * data['volume']).cumsum()
        vwap_denominator = data['volume'].cumsum()
        data['VWAP'] = vwap_numerator / vwap_denominator
    return data