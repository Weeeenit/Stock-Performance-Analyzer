import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    get_stock_list,
    load_stock,
    filter_data,
    calculate_daily_returns,
    calculate_cumulative_returns,
    calculate_monthly_returns,
    calculate_yearly_returns,
    get_return_statistics
)

st.title("Return Analysis")

# =====================================================
# Sidebar
# =====================================================

stocks = get_stock_list()

stock = st.sidebar.selectbox(
    "Select Stock",
    stocks,
    key="return_stock"
)

df = load_stock(stock)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="return_date"
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df = filter_data(df, start_date, end_date)

# =====================================================
# Calculations
# =====================================================

df = calculate_daily_returns(df)
df = calculate_cumulative_returns(df)

stats = get_return_statistics(df)

# =====================================================
# KPI Cards
# =====================================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Average Return", f"{stats['Average Return']:.2f}%")
c2.metric("Median Return", f"{stats['Median Return']:.2f}%")
c3.metric("Best Day", f"{stats['Maximum Return']:.2f}%")
c4.metric("Worst Day", f"{stats['Minimum Return']:.2f}%")
c5.metric("Volatility", f"{stats['Volatility']:.2f}%")

st.divider()

# =====================================================
# Daily Return Distribution
# =====================================================

st.subheader("Daily Return Distribution")

fig = px.histogram(
    df,
    x="Daily Return",
    nbins=60,
    title="Distribution of Daily Returns"
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    bargap=0.05
)

st.plotly_chart(fig, width="stretch")

st.divider()

# =====================================================
# Cumulative Returns
# =====================================================

st.subheader("Cumulative Return")

fig = px.line(
    df,
    x="Date",
    y="Cumulative Return"
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    hovermode="x unified"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# =====================================================
# Monthly Return Heatmap
# =====================================================

# st.subheader("Monthly Return Heatmap")

# heatmap = calculate_monthly_returns(df)

# fig = go.Figure(
#     data=go.Heatmap(
#         z=heatmap.values,
#         x=heatmap.columns,
#         y=heatmap.index,
#         colorscale="RdYlGn",
#         colorbar_title="% Return",
#         hoverongaps=False
#     )
# )

# fig.update_layout(
#     template="plotly_dark",
#     height=500
# )

# st.plotly_chart(fig, width="stretch")

# st.divider()

# =====================================================
# Yearly Returns
# =====================================================

st.subheader("Yearly Returns")

yearly = calculate_yearly_returns(df)

fig = px.bar(
    x=yearly.index.astype(str),
    y=yearly.values,
    labels={
        "x": "Year",
        "y": "Return (%)"
    }
)

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig, width="stretch")

st.divider()

# =====================================================
# Best and Worst Trading Day
# =====================================================

st.subheader("Best and Worst Trading Day")

best_day = df.loc[df["Daily Return"].idxmax()]
worst_day = df.loc[df["Daily Return"].idxmin()]

left, right = st.columns(2)

with left:

    st.success("Best Trading Day")

    st.write(f"Date : {best_day['Date'].date()}")
    st.write(f"Return : {best_day['Daily Return']:.2f}%")
    st.write(f"Closing Price : ₹{best_day['Close']:.2f}")

with right:

    st.error("Worst Trading Day")

    st.write(f"Date : {worst_day['Date'].date()}")
    st.write(f"Return : {worst_day['Daily Return']:.2f}%")
    st.write(f"Closing Price : ₹{worst_day['Close']:.2f}")