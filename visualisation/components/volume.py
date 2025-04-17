import seaborn as sns

def plot_volume(data, ax):
    """Plots the volume bar chart on the given axis."""
    ax.bar(data['date'], data['volume'], color=sns.color_palette()[0], width=0.8)