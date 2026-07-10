import streamlit as st
import plotly.express as px

from utils import (
    get_stock_list,
    load_stock,
    filter_data,
    calculate_kpis,
    calculate_statistics
)

st.title("Stock Performance Analyzer")

# ==============================
# Sidebar
# ==============================

stocks = get_stock_list()

stock = st.sidebar.selectbox(
    "Select Stock",
    stocks
)

df = load_stock(stock)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = filter_data(df, start_date, end_date)

# ==============================
# KPI Cards
# ==============================

kpi = calculate_kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"₹{kpi['Current Price']:.2f}"
)

col2.metric(
    "Highest Price",
    f"₹{kpi['Highest Price']:.2f}"
)

col3.metric(
    "Lowest Price",
    f"₹{kpi['Lowest Price']:.2f}"
)

col4.metric(
    "Total Return",
    f"{kpi['Total Return']:.2f}%"
)

st.divider()

# ==============================
# Price Chart
# ==============================

st.subheader("Closing Price")

fig = px.line(
    df,
    x="Date",
    y="Close"
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Date",
    yaxis_title="Closing Price",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# ==============================
# Volume Chart
# ==============================

st.subheader("Trading Volume")

fig = px.bar(
    df,
    x="Date",
    y="Volume"
)

fig.update_layout(
    template="plotly_dark",
    height=400,
    xaxis_title="Date",
    yaxis_title="Volume"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# ==============================
# Statistics
# ==============================

stats = calculate_statistics(df)

st.subheader("Trading Statistics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Trading Days",
    f"{stats['Trading Days']:,}"
)

c2.metric(
    "Average Close",
    f"₹{stats['Average Close']:.2f}"
)

c3.metric(
    "Average Volume",
    f"{stats['Average Volume']:,.0f}"
)

c4, c5 = st.columns(2)

c4.metric(
    "Highest Volume",
    f"{stats['Highest Volume']:,.0f}"
)

c5.metric(
    "Highest Price",
    f"₹{stats['Highest Price']:.2f}"
)

st.divider()

# ==============================
# Latest Records
# ==============================

st.subheader("Latest Trading Records")

display_df = (
    df.sort_values("Date", ascending=False)
      .head(10)
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# ==============================
# Download
# ==============================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Data",
    csv,
    file_name=f"{stock}.csv",
    mime="text/csv"
)