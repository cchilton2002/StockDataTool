import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import NullFormatter
from typing import Optional

from analysis import CalculateIndicators
from visualisation.components import (
    plot_candlestick,
    plot_line,
    plot_volume,
    plot_rsi,
    plot_indicator  # This wraps plot_ma, plot_bb, plot_vwap
)

class StockPlotter:
    def __init__(self, data: pd.DataFrame, ticker: str, start_date: str, end_date: str):
        self.data = data.copy()
        self.ticker = ticker
        self.start_date = pd.to_datetime(start_date).date()
        self.end_date = pd.to_datetime(end_date).date()

    def _filter_data(self) -> pd.DataFrame:
        self.data['date'] = pd.to_datetime(self.data['date']).dt.date
        return self.data[
            (self.data['date'] >= self.start_date) & (self.data['date'] <= self.end_date)
        ].copy()

    def _apply_indicators(self, ma: bool, bb: bool, vwap: bool, rsi: bool):
        calc = CalculateIndicators(self.data)
        calc.calculate(ma=ma, bb=bb, vwap=vwap, rsi=rsi)
        self.data = calc.get_data()

    def plot(self, ma: bool = False, bb: bool = False, vwap: bool = False, rsi: bool = False) -> None:
        self._apply_indicators(ma, bb, vwap, rsi)
        self.filtered_data = self._filter_data()

        sns.set_style("whitegrid")
        sns.set_palette("viridis")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
        fig.suptitle(f"Stock Price for {self.ticker.upper()}", fontsize=35)

        # Plot price and volume
        plot_candlestick(self.filtered_data, ax1)
        plot_line(self.filtered_data, ax1)
        plot_volume(self.filtered_data, ax2)

        # Plot selected indicators
        if any([ma, bb, vwap]):
            if ma:
                plot_indicator(self.filtered_data, ax1, "ma")
            if bb:
                plot_indicator(self.filtered_data, ax1, "bb")
            if vwap:
                plot_indicator(self.filtered_data, ax1, "vwap")
            ax1.legend(fontsize=20)
            
        # Plot RSI on twin axis if selected
        if rsi and "RSI" in self.filtered_data:
            ax3 = ax2.twinx()
            plot_rsi(self.filtered_data, ax3)
            ax3.set_ylabel("RSI", fontsize=25, color="orange")
            ax3.tick_params(axis="y", labelsize=18)
            ax3.legend(loc="upper right", fontsize=18)

        # Format axes
        for ax in [ax1, ax2]:
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.tick_params(axis="y", labelsize=18)
            ax.tick_params(axis="x", labelsize=18)

        ax1.set_ylabel("Stock Price ($)", fontsize=25)
        ax2.set_ylabel("Volume", fontsize=25)
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        ax1.xaxis.set_minor_formatter(NullFormatter())

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('example_plot.png', dpi=300, bbox_inches='tight')
        plt.show()
