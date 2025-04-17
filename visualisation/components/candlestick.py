def plot_candlestick(data, ax):
    """Plots a candlestick chart on the given axis."""
    bar_width = 1
    wick_width = 1.5
    
    for date, open_, close, low, high in zip(data['date'], data['open'], data['close'], data['low'], data['high']):
        color = 'green' if close > open_ else 'red'
        ax.vlines(x=date, ymin=low, ymax=high, color=color, linewidth=wick_width)
        ax.bar(x=date, bottom=min(open_, close), height=abs(close - open_), color=color, width=bar_width)