import pandas as pd
import numpy as np

class CalculateIndicators:
    def __init__(self, data:pd.DataFrame):
        self.data = data.copy()
    
    def calculate_sma(self, window: int = 200) -> pd.Series:
        self.data[f"SMA_{window}"] = self.data["close"].rolling(window=window).mean()
        return self.data[f"SMA_{window}"]
    
    def calculate_ema(self, window: int = 200) -> pd.Series:
        self.data[f"EMA_{window}"] = self.data["close"].ewm(span=200, adjust=False).mean()
        return self.data[f"EMA_{window}"]
    
    def calculate_bollinger_bands(self, window: int = 20, num_std: float = 2.0) -> pd.Series:
        sma = self.data["close"].rolling(window=window).mean()
        std = self.data["close"].rolling(window=window).std()
        self.data["BB_upper"] = sma + num_std * std
        self.data["BB_lower"] = sma - num_std * std
        self.data[f"SMA_{window}"] = sma
        return self.data[["BB_upper", "BB_lower", f"SMA_{window}"]]
    
    def calculate_rsi(self, window: int = 14) -> pd.Series:
        delta = self.data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.data["RSI"] = 100 - (100 / (1 + rs))
        return self.data["RSI"]
    
    def calculate_vwap(self) -> pd.Series:
        typical_price = (self.data["high"] + self.data["low"] + self.data["close"]) / 3
        vwap = (typical_price * self.data["volume"]).cumsum() / self.data["volume"].cumsum()
        self.data["VWAP"] = vwap
        return vwap
    
    def calculate(self, ma: bool = False, bb: bool = False, 
                 vwap: bool = False, rsi: bool = False) -> pd.DataFrame:
        """Calculate indicators in-place (no return)"""
        if ma:
            self.calculate_sma()
            self.calculate_ema()
        if bb:
            self.calculate_bollinger_bands()
        if vwap:
            self.calculate_vwap()
        if rsi:
            self.calculate_rsi()
        return self.data.copy()

    def get_data(self) -> pd.DataFrame:
        """Explicit accessor for the calculated data"""
        return self.data.copy()
        