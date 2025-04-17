# visualisation/plot_indicators.py

def plot_ma(data, ax):
    ax.plot(data['date'], data["SMA_200"], color="red", linestyle='-', linewidth=2, label="SMA 200", alpha=0.8) 
    ax.plot(data['date'], data["EMA_200"], linestyle='--', linewidth=2, label="EMA 200", alpha=0.8)

def plot_bb(data, ax):
    ax.plot(data['date'], data["SMA_20"], linestyle='--', color="purple", linewidth=1.7, label="SMA 20")
    ax.plot(data['date'], data["BB_upper"], linestyle='-', color="orangered", linewidth=1.1, label="BB Upper")
    ax.plot(data['date'], data["BB_lower"], linestyle='-', color="limegreen", linewidth=1.1, label="BB Upper")
    ax.fill_between(data['date'], data["BB_upper"], data["BB_lower"], color='purple', alpha=0.1, label="BB Range")

def plot_vwap(data, ax):
    ax.plot(data['date'], data['VWAP'], color="gold", linewidth=2, linestyle="--", label="VWAP")
    
def plot_rsi(data, ax):
    """Plots the RSI indicator on a secondary y-axis (overlapping volume)."""
    
    ax.plot(data['date'], data['RSI'], color="orange", linewidth=2, label="RSI")
    ax.axhline(70, linestyle="--", color="red", alpha=0.7)
    ax.axhline(30, linestyle="--", color="green", alpha=0.7)
    
    ax.set_ylim(0, 100)
    ax.tick_params(axis='y', labelsize=14, colors="orange")
    
def plot_indicator(ax, data, indicator_type):
    """Plot a single indicator. No need for .lower() since types are lowercase."""
    if indicator_type == "ma":
        plot_ma(ax, data)
    elif indicator_type == "bb":
        plot_bb(ax, data)
    elif indicator_type == "vwap":
        plot_vwap(ax, data)
    else:
        raise ValueError(f"Unsupported indicator: {indicator_type}")

