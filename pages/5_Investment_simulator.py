import streamlit as st
import plotly.express as px
import pandas as pd

from utils import (
    get_stock_list,
    load_stock,
    investment_simulator,
    investment_growth
)

st.title("Investment Simulator")

# =====================================================
# Sidebar
# =====================================================

stocks = get_stock_list()

stock = st.sidebar.selectbox(
    "Select Stock",
    stocks,
    key="investment_stock"
)

df = load_stock(stock)

# =====================================================
# User Inputs
# =====================================================

investment = st.sidebar.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    max_value=10000000,
    value=10000,
    step=1000
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

investment_date = st.sidebar.date_input(
    "Investment Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

# =====================================================
# Filter Data
# =====================================================

df = df[df["Date"] >= pd.to_datetime(investment_date)].copy()

if len(df) < 2:
    st.warning("Please choose an earlier investment date.")
    st.stop()

# =====================================================
# Investment Calculations
# =====================================================

results = investment_simulator(df, investment)

growth_df = investment_growth(df, investment)

shares = investment / df["Close"].iloc[0]

holding_days = (
    growth_df["Date"].iloc[-1] - growth_df["Date"].iloc[0]
).days

# =====================================================
# KPI Cards
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Investment",
    f"₹{investment:,.0f}"
)

c2.metric(
    "Current Value",
    f"₹{results['Current Value']:,.2f}"
)

c3.metric(
    "Profit / Loss",
    f"₹{results['Profit']:,.2f}"
)

c4.metric(
    "CAGR",
    f"{results['CAGR']:.2f}%"
)

st.divider()

# =====================================================
# Portfolio Growth
# =====================================================

st.subheader("Portfolio Value Over Time")

fig = px.line(
    growth_df,
    x="Date",
    y="Portfolio Value"
)

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified",
    height=500,
    xaxis_title="Date",
    yaxis_title="Portfolio Value (₹)"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# =====================================================
# Investment Summary
# =====================================================

st.subheader("Investment Summary")

left, right = st.columns(2)

with left:

    st.metric(
        "Shares Purchased",
        f"{shares:.2f}"
    )

    st.metric(
        "Purchase Price",
        f"₹{df['Close'].iloc[0]:.2f}"
    )

    st.metric(
        "Latest Price",
        f"₹{df['Close'].iloc[-1]:.2f}"
    )

with right:

    st.metric(
        "Holding Period",
        f"{holding_days} Days"
    )

    st.metric(
        "Total Return",
        f"{results['Return']:.2f}%"
    )

    st.metric(
        "Net Profit",
        f"₹{results['Profit']:,.2f}"
    )

st.divider()

# =====================================================
# Portfolio History
# =====================================================

st.subheader("Portfolio History")

portfolio = growth_df[
    ["Date", "Close", "Portfolio Value"]
].copy()

portfolio.columns = [
    "Date",
    "Closing Price",
    "Portfolio Value"
]

st.dataframe(
    portfolio.tail(15),
    width="stretch",
    hide_index=True
)

# =====================================================
# Download
# =====================================================

csv = portfolio.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Portfolio History",
    data=csv,
    file_name=f"{stock}_portfolio.csv",
    mime="text/csv"
)