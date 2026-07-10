import streamlit as st
import plotly.graph_objects as go

from utils import (
    get_stock_list,
    load_stock,
    filter_data,
    add_moving_averages,
    calculate_bollinger_bands,
    get_trend
)

st.title("Price Analysis")

# ==========================================
# Sidebar
# ==========================================

stocks = get_stock_list()

stock = st.sidebar.selectbox(
    "Select Stock",
    stocks,
    key="price_stock"
)

df = load_stock(stock)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="price_date"
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = filter_data(df, start_date, end_date)

df = add_moving_averages(df)
df = calculate_bollinger_bands(df)

# ==========================================
# Chart Options
# ==========================================

chart_type = st.sidebar.radio(
    "Chart Type",
    ["Line", "Candlestick"]
)

show_ma20 = st.sidebar.checkbox("20 Day MA", True)
show_ma50 = st.sidebar.checkbox("50 Day MA", True)
show_ma200 = st.sidebar.checkbox("200 Day MA", False)
show_bb = st.sidebar.checkbox("Bollinger Bands", False)

# ==========================================
# Trend
# ==========================================

trend = get_trend(df)

st.metric("Current Trend", trend)

st.divider()

# ==========================================
# Price Chart
# ==========================================

fig = go.Figure()

if chart_type == "Candlestick":

    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        )
    )

else:

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=3)
        )
    )

if show_ma20:

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA20"],
            name="20 MA"
        )
    )

if show_ma50:

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA50"],
            name="50 MA"
        )
    )

if show_ma200:

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA200"],
            name="200 MA"
        )
    )

if show_bb:

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Upper Band"],
            name="Upper Band",
            line=dict(dash="dot")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Lower Band"],
            name="Lower Band",
            line=dict(dash="dot")
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=650,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# ==========================================
# Price Statistics
# ==========================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Highest Price",
    f"₹{df['High'].max():.2f}"
)

col2.metric(
    "Lowest Price",
    f"₹{df['Low'].min():.2f}"
)

col3.metric(
    "Average Close",
    f"₹{df['Close'].mean():.2f}"
)

st.divider()

# ==========================================
# Technical Summary
# ==========================================

summary = {
    "Current Price": df["Close"].iloc[-1],
    "20 MA": df["MA20"].iloc[-1],
    "50 MA": df["MA50"].iloc[-1],
    "200 MA": df["MA200"].iloc[-1]
}

st.subheader("Technical Summary")

st.dataframe(
    summary,
    width="stretch"
)