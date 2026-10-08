import matplotlib.pyplot as plt
import pandas as pd
from analysis import category_totals, location_totals, dataframe

# One main colour for every graph - matches the GUI theme.
TEAL = '#00A6A6'
BG = '#F7F9FC'
NAVY = '#17324D'


def style_chart(title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor('white')
    ax.set_title(title, fontsize=16, fontweight='bold', color=NAVY, pad=15)
    ax.set_xlabel(xlabel, fontsize=11, color=NAVY)
    ax.set_ylabel(ylabel, fontsize=11, color=NAVY)
    ax.grid(axis='y', linestyle='--', alpha=0.20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.20)
    ax.spines['bottom'].set_alpha(0.20)
    return fig, ax


def show_category_chart():
    data = category_totals()
    if data.empty:
        return

    fig, ax = style_chart(
        'Total Waste Collected by Category',
        'Waste Category',
        'Quantity (kg)'
    )
    bars = ax.bar(data.index, data.values, color=TEAL, width=0.62)
    ax.bar_label(bars, fmt='%.1f kg', padding=4, fontsize=9, color=NAVY)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def show_location_chart():
    data = location_totals()
    if data.empty:
        return

    fig, ax = style_chart(
        'Total Waste Collected by Location',
        'Location',
        'Quantity (kg)'
    )
    bars = ax.bar(data.index, data.values, color=TEAL, width=0.62)
    ax.bar_label(bars, fmt='%.1f kg', padding=4, fontsize=9, color=NAVY)
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.show()


def show_time_graph():
    df = dataframe()
    if df.empty:
        return

    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby('date')['quantity'].sum()

    fig, ax = style_chart(
        'Waste Collection Over Time',
        'Date',
        'Quantity (kg)'
    )

    # Same teal colour as both bar charts.
    ax.plot(
        daily.index,
        daily.values,
        marker='o',
        linewidth=2.5,
        markersize=7,
        color=TEAL
    )
    ax.fill_between(daily.index, daily.values, alpha=0.10, color=TEAL)

    for x, y in zip(daily.index, daily.values):
        ax.annotate(
            f'{y:.0f}',
            (x, y),
            textcoords='offset points',
            xytext=(0, 8),
            ha='center',
            fontsize=8,
            color=NAVY
        )

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()
